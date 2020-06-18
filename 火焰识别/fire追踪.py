import cv2
import numpy as np
import time
import threading
from datetime import datetime
import sortMOT
import os.path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io
from sklearn.utils.linear_assignment_ import linear_assignment
import glob
import argparse
from filterpy.kalman import KalmanFilter

def panju(image):
    cv2.imshow('tagimage', image)
    dt = datetime.now()
    a=dt.strftime('%H%M%S')
    cv2.imwrite("C:/"+str(a)+".png",image)
    print("写入成功")
    #cv2.waitKey()
def IOU( box1, box2 ):

    width1 = abs(box1[2] - box1[0])
    height1 = abs(box1[1] - box1[3]) # 这里y1-y2是因为一般情况y1>y2，为了方便采用绝对值
    width2 = abs(box2[2] - box2[0])
    height2 = abs(box2[1] - box2[3])
    x_max = max(box1[0],box1[2],box2[0],box2[2])
    y_max = max(box1[1],box1[3],box2[1],box2[3])
    x_min = min(box1[0],box1[2],box2[0],box2[2])
    y_min = min(box1[1],box1[3],box2[1],box2[3])
    iou_width = x_min + width1 + width2 - x_max
    iou_height = y_min + height1 + height2 - y_max
    if iou_width <= 0 or iou_height <= 0:
        iou_ratio = 0
    else:
        iou_area = iou_width * iou_height # 交集的面积
        box1_area = width1 * height1
        box2_area = width2 * height2
        iou_ratio = iou_area / (box1_area + box2_area - iou_area) # 并集的面积
    return iou_ratio

mot_tracker = sortMOT.Sort()
# 构建卡尔曼滤波器
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)#c测量矩阵
kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)#转移矩阵
kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                                       np.float32) * 0.03#噪声协方差矩阵
measurement = np.array((2, 1), np.float32)
prediction = np.zeros((2, 1), np.float32)
currentwidow=[]

#设定红色阈值黄色阈值蓝色的阈值绿色阈值，HSV空间
lower_red = np.array([170, 150, 50])
upper_red = np.array([179, 255, 255])
lower_yellow = np.array([26, 50, 50])
upper_yellow = np.array([34, 255, 255])
lower_blue = np.array([110,100,100])
upper_blue = np.array([130,255,255])
lower_green = np.array([35,150,100])
upper_green = np.array([75,255,255])


#指定写视频的格式, I420-avi, MJPG-mp4
# fps=25
# size=640,480
# out_frame = cv2.VideoWriter('c://color_track.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
# out_hsv = cv2.VideoWriter('c://color_detect_hsv.avi', cv2.VideoWriter_fourcc(*'MP42'), fps, size)
# out_mask = cv2.VideoWriter('c://color_detect_mask.avi', cv2.VideoWriter_fourcc(*'MP42'), fps, size)

#打开摄像头

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("F:/python/学习练习/fire/20191120_162459.mp4")
#等待两秒
time.sleep(2)

args = sortMOT.parse_args()
display = args.display
total_time = 0.0
total_frames = 0
colours = np.random.rand(32, 3)  # used only for display
if (display):
    if not os.path.exists('mot_benchmark'):
        print(
            '\n\tERROR: mot_benchmark link not found!\n\n    Create a symbolic link to the MOT benchmark\n    (https://motchallenge.net/data/2D_MOT_2015/#download). E.g.:\n\n    $ ln -s /path/to/MOT2015_challenge/2DMOT2015 mot_benchmark\n\n')
        exit()
    plt.ion()
    fig = plt.figure()

if not os.path.exists('output'):
    os.makedirs('output')

while (1):
    (ret, frame) = cap.read()
    if not ret:
        print ('No Camera\n')
        break
    start_time = time.time()
    #转到绿色的HSV空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #根据阈值构建蒙版掩膜
    #mask = cv2.inRange(hsv, lower_red, upper_red)
    #mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    #用红色的蒙版
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    # 用黄色的蒙版
    mask_yellow = cv2.inRange(hsv, lower_red, upper_red)
    # 膨胀操作，去除噪点
    # mask_green = cv2.erode(mask_green, None, iterations=2)
    # mask_green = cv2.dilate(mask_green, None, iterations=3)
    # mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
    # mask_yellow = cv2.dilate(mask_yellow, None, iterations=3)
    # mask_red = cv2.erode(mask_red, None, iterations=2)
    # mask_red = cv2.dilate(mask_red, None, iterations=3)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=3)
    mask = mask_green+mask_red+mask_yellow
    #最大面积和最小面积阈值
    min_thresh = 1000
    max_thresh = 60000
    output = cv2.connectedComponentsWithStats(mask,8, cv2.CV_32S)
    # _, labels, stats, centroids.
    # stats 是bounding box的信息，N*5的矩阵，行对应每个label，五列分别为[x0, y0, width, height, area]
    # centroids 是每个域的质心坐标
    contlist=[]
    lastwindow=currentwidow#保存一下上一帧的框框
    print("上帧追踪框参数",lastwindow)


    for i in range(output[0]):
        jj=[]
        if output[2][i][4] >= min_thresh and output[2][i][4] <= max_thresh:
            #cv2.rectangle(frame, (output[2][i][0], output[2][i][1]), (output[2][i][0] + output[2][i][2], output[2][i][1] + output[2][i][3]), (0, 255, 0), 2)
            jj=list(output[2][i])
            jj.append(list(output[3][i]))
            jj.append(i)
            #jj=[x0, y0, width, height, area,centroids,i]
            contlist.append(jj)
            #print(jj)
    # contlist=[[x0, y0, width, height, area,centroids,i],[x0, y0, width, height, area,centroids,i]]
    if len(contlist)>=1:
        listance = []
        maxte=[]
        currentwidow=[]#[[x,y,w,h,id],[]]
        for i in range(0,len(contlist)):
            j = i
            while j + 1 < len(contlist):
                # print(contlist)
                # print(contlist[i])
                # print(contlist[i][5][0])
                d =np.abs(int(contlist[i][5][0])-int(contlist[j+1][5][0]))+ np.abs(int(contlist[i][5][1])-int(contlist[j+1][5][1]))
                #print(d)
                if d<300:   #j距离阈值
                    #找出两个区域合并后矩形的参数
                    x = min([contlist[i][0], contlist[j + 1][0]])
                    y = min([contlist[i][1], contlist[j + 1][1]])
                    w = contlist[i][2]+contlist[j + 1][2]
                    h = contlist[i][3]+contlist[j + 1][3]
                    # 把两个区域的的面积 全放到 后面的元素上
                    contlist[j + 1][0] = x
                    contlist[j + 1][1] = y
                    contlist[j + 1][2] = w
                    contlist[j + 1][3] = h
                    contlist[j + 1][6] = contlist[i][6]
                    contlist.remove(contlist[i])

                j=j+1

        # 把conlist中的每个框的id变成从0开始
        for i in range(len(contlist)):
            contlist[i][6]=i

        currentwidow=contlist[:]

        print("本帧追踪框参数",currentwidow)
        for id in range(0,len(currentwidow)):
            cv2.rectangle(frame, (currentwidow[id][0], currentwidow[id][1]), (currentwidow[id][0] +currentwidow[id][2], currentwidow[id][1] +currentwidow[id][3]), (0, 255, 0), 2)

            roi=frame[currentwidow[id][1]:currentwidow[id][1] + currentwidow[id][3],currentwidow[id][0]:currentwidow[id][0] + currentwidow[id][2]]
            currentcenter=np.array([np.float32(currentwidow[id][0]+currentwidow[id][2]/2),np.float32(currentwidow[id][1]+currentwidow[id][3]/2)], np.float32)
            #卡尔曼滤波应用
            kalman.correct(currentcenter)
            predictioncenter = kalman.predict()

            for q in range(len(lastwindow)):
                # box1=(lastwindow[q][1],lastwindow[q][0],lastwindow[q][1] + lastwindow[q][3],lastwindow[q][0]+lastwindow[q][2])
                # box2=(predictioncenter[1]-lastwindow[q][3],predictioncenter[0]-lastwindow[q][2],predictioncenter[1]+lastwindow[q][3],predictioncenter[0]+lastwindow[q][2])
                box1=(lastwindow[q][0],lastwindow[q][1],lastwindow[q][0]+lastwindow[q][2],lastwindow[q][1] + lastwindow[q][3])
                box2=(predictioncenter[0]-lastwindow[q][2]/2,predictioncenter[1]-lastwindow[q][3]/2,predictioncenter[0]+lastwindow[q][2]/2,predictioncenter[1]+lastwindow[q][3]/2)
                iou=IOU(box1,box2)
                print("iou（（矩形框交并比））：",iou)
                detection=box1[:]
                detection=list(detection)
                detection.append(lastwindow[q][6])
                detection=np.array(detection)

                detection=detection.reshape(1,5)

                mot_tracker.update(detection)

                op2 = np.linalg.norm(currentcenter -predictioncenter)
                if op2<50:
                    currentwidow[id][6]=lastwindow[q][6]

                print("距离值：",op2)

            cv2.circle(frame, (int(predictioncenter[0]), int(predictioncenter[1])), 4, (255, 0, 0), -1)

            if total_frames%5==0:
                t1 = threading.Thread(target=panju, args=(roi,))
                t1.start()
                t1.join()

    if len(contlist)== 1:
        cv2.rectangle(frame, (contlist[0][0], contlist[0][1]),(contlist[0][0] + contlist[0][2], contlist[0][1] + contlist[0][3]), (0, 255, 0), 2)
    if len(contlist)==0:
        cv2.putText(frame, "未发现可疑目标！", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    print("      ")

    cv2.imshow('Frame', frame)
    #cv2.imshow('Frame_hsv', hsv)
    #.imshow('Frame_mask', mask)

    #out_frame.write(frame)
    #out_hsv.write(hsv)
    #out_mask.write(mask)
    #esc键退出
    if cv2.waitKey(5) == 27 or cv2.waitKey(5) == ord('q'):
        print('exit!\n')
        break
    total_frames+=1
    cycle_time = time.time() - start_time
    total_time += cycle_time

cap.release()
cv2.destroyAllWindows()


