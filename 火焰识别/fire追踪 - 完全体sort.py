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
#import detection_bboxpre
import torch
import torchvision.models
from torchvision import transforms
from PIL import Image
import sortMOT_V2
def panju(image):
    cv2.imshow('tagimage', image)
    dt = datetime.now()
    a=dt.strftime('%H%M%S')
    cv2.imwrite("C:/"+str(a)+".png",image)
    print("写入成功")
    #cv2.waitKey()

mot_tracker = sortMOT_V2.Sort()
currentwidow=[]

#设定红色阈值黄色阈值蓝色的阈值绿色阈值，HSV空间
hsv_fire_low1=np.array([5,128,205])
hsv_fire_high1=np.array([33,255,255])

rgb_fire_low1=np.array([200,50,0])
rgb_fire_high1=np.array([255,255,125])


#指定写视频的格式, I420-avi, MJPG-mp4
# fps=25
# size=640,480
# out_frame = cv2.VideoWriter('c://color_track.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
# out_hsv = cv2.VideoWriter('c://color_detect_hsv.avi', cv2.VideoWriter_fourcc(*'MP42'), fps, size)
# out_mask = cv2.VideoWriter('c://color_detect_mask.avi', cv2.VideoWriter_fourcc(*'MP42'), fps, size)

#打开摄像头

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\car3.mp4")
#等待两秒
masknew=cap.read()[1]
print(masknew.shape)
a, b ,c= masknew.shape
min_thresh = 0.005 * a * b
max_thresh = 0.75 * a * 0.75 * b
sthord = 0.2*max(a,b)

net = torch.load('D:/zhaopro/fire/model18.pkl')
normalize = transforms.Normalize(mean=[0.485], std=[0.229])
train_transformer_ImageNet = transforms.Compose([
    transforms.RandomResizedCrop(112),
    transforms.Grayscale(1),
    #transforms.ColorJitter(contrast=(2,3)),
    transforms.ToTensor(),
    #normalize
])

def classification(frame):
    imm = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    frame=train_transformer_ImageNet(imm)
    imm2 = torch.unsqueeze(frame, dim=0).float()
    output1 = net(imm2)
    _, predicted = torch.max(output1.data, 1)
    return predicted



frquency=cv2.getTickFrequency()
#print(frquency)
total_time = 0.0
total_frames = 0
trackers=[]#初始化trackers
jiluzhuangtai={}#记录每一个id是否为火焰，0为火焰，1为非火焰

colortime=0
tracktime=0
classfictime=0
classfictcount=0
while (1):
    (ret, frame) = cap.read()
    if not ret:
        print ('No Camera\n')
        break
    lastwindow=trackers#保存一下上一帧的框框
    lastid=[]
    for i in lastwindow:
        lastid.append(i[4])
    print("上一帧id",lastid)


    start_time=cv2.getTickCount()
    sstart_time = time.time()

    #frame = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    print("创建mask前时间", time.time() - sstart_time)
    hsv_mask1 = cv2.inRange(hsv, hsv_fire_low1, hsv_fire_high1)
    rgb_mask1 = cv2.inRange(rgb, rgb_fire_low1, rgb_fire_high1)
    mask=hsv_mask1+rgb_mask1
    print("创建mask时间",time.time()-sstart_time)

    #最大面积和最小面积阈值
    output = cv2.connectedComponentsWithStats(mask,8, cv2.CV_32S)
    # _, labels, stats, centroids.
    # stats 是bounding box的信息，N*5的矩阵，行对应每个label，五列分别为[x0, y0, width, height, area]
    # centroids 是每个域的质心坐标
    print("创建mask后时间", time.time() - sstart_time)

    #print("上帧追踪框参数",lastwindow)
    #print(output)
    initalbox=output[2]
    sfliterbox = initalbox[initalbox[:, 4] <=max_thresh]
    sfliterbox= sfliterbox[sfliterbox[:, 4] >= min_thresh]
    print("面积筛选时间", time.time() - sstart_time)
    #print("数组出来的",sfliterbox)
    # for i in range(output[0]):
    #     jj=[]
    #     if output[2][i][4] >= min_thresh and output[2][i][4] <= max_thresh:
    #         jj=list(output[2][i])
    #         jj.append(list(output[3][i]))
    #         jj.append(i)
    #         #jj=[x0, y0, width, height, area,centroids,i]
    #         contlist.append(jj)
    # contlist=[[x0, y0, width, height, area,centroids,i],[x0, y0, width, height, area,centroids,i]]

    sfliterbox[:,2:4]+=sfliterbox[:,0:2]
    #print(sfliterbox)
    if len(sfliterbox)>=1:
        listance = []
        maxte=[]
        currentwidow=[]#[[x,y,w,h,id],[]]
        for i in range(0,len(sfliterbox)):
            j = i
            while j + 1 < len(sfliterbox):
                d=sortMOT.iou(sfliterbox[i],sfliterbox[j+1])
                #曼哈顿距离
                #d =np.abs(int(contlist[i][5][0])-int(contlist[j+1][5][0]))+ np.abs(int(contlist[i][5][1])-int(contlist[j+1][5][1]))
                #print(d)
                if d>0:   #iou阈值
                    aa = frame[sfliterbox[i][1]:sfliterbox[i][3], sfliterbox[i][0]:sfliterbox[i][2]]
                    bb = frame[sfliterbox[j + 1][1]:sfliterbox[j + 1][3], sfliterbox[j + 1][0]:sfliterbox[j + 1][2]]
                    saa=(sfliterbox[i][3]-sfliterbox[i][1])*(sfliterbox[i][2]-sfliterbox[i][0])
                    sbb=(sfliterbox[j + 1][3]-sfliterbox[j + 1][1])*(sfliterbox[j + 1][2]-sfliterbox[j + 1][0])
                    histaa = cv2.calcHist(aa, [0], None, [32], [0, 255])
                    histbb = cv2.calcHist(bb, [0], None, [32], [0, 255])

                    hist_mask1, bins1 = np.histogram(aa.ravel(), 32, [0, 256])
                    hist_mask2, bins2 = np.histogram(bb.ravel(), 32, [0, 256])

                    hist_mask1 = (hist_mask1 / float(saa)).astype(np.float32)
                    hist_mask2 = (hist_mask2 / float(sbb)).astype(np.float32)

                    dist=cv2.compareHist(hist_mask1, hist_mask2, cv2.HISTCMP_CORREL)

                    print(dist)
                    #dist = np.linalg.norm(histaa - histbb) / (contlist[i][3] * contlist[i][2])

                    if dist > 0.1:

                    #找出两个区域合并后矩形的参数
                        x1 = min([sfliterbox[i][0], sfliterbox[j + 1][0]])
                        y1 = min([sfliterbox[i][1], sfliterbox[j + 1][1]])
                        x2 = max([sfliterbox[i][2], sfliterbox[j + 1][2]])
                        y2 = max([sfliterbox[i][3], sfliterbox[j + 1][3]])
                        # 把两个区域的的面积 全放到 后面的元素上
                        sfliterbox[j + 1][0] = x1
                        sfliterbox[j + 1][1] = y1
                        sfliterbox[j + 1][2] = x2
                        sfliterbox[j + 1][3] = y2

                        sfliterbox[i][4]=0

                        #sfliterbox.remove(sfliterbox[i])

                j=j+1
        sfliterbox=sfliterbox[sfliterbox[:, 4] >0]

        colorend=(cv2.getTickCount()-start_time)/frquency
        colortime+=colorend



        print("框合并时间", time.time() - sstart_time)
        # # 把conlist中的每个框的id变成从0开始
        # for i in range(len(sfliterbox)):
        #     sfliterbox[i][6]=i
        #     guodu= sfliterbox[i][:4]
        #     guodu.append(sfliterbox[i][6])
        #     guodu=np.array(guodu)
        #     currentwidow.append(guodu)

        detectiontime =cv2.getTickCount()
        print("detection时间",(detectiontime-start_time)/frquency)

        # #print("本帧追踪框参数",currentwidow)
        # detection=np.array(currentwidow)
        # detection[:, 2:4] += detection[:, 0:2]
        # print(detection)

        trackers = mot_tracker.update(sfliterbox)
        trackers=trackers.astype(int)




        for d in trackers:
            #print (type(int(d[4])))
            caijiantu=frame[int(d[1]):int(d[3]),int(d[0]):int(d[2])]
            if (int(d[3])-int(d[1]))<=0 or (int(d[2])-int(d[0]))<=0:
                continue
            # isfire=detection_bboxpre.classification(caijiantu)
            cv2.rectangle(frame, (int(d[0]), int(d[1])), (int(d[2]), int(d[3])), (0, 255, 0), 2)

            biaoji=str(d[4])

            if d[4] in lastid:
                print("重复id", d[4])
                if jiluzhuangtai[d[4]]==0:
                    cv2.putText(frame, 'fire', (int(d[0])+50, int(d[1])), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            else:
                fenleiqian=cv2.getTickCount()
                a=classification(caijiantu)
                fenleihou=cv2.getTickCount()
                classfictcount+=1
                classfictime+=(fenleihou-fenleiqian)/frquency
                print("分类所用时间",(fenleihou-fenleiqian)/frquency)
                jiluzhuangtai[d[4]]=a
                # if a==0:
                #     cv2.putText(frame, '火焰', (int(d[0]), int(d[1])), cv2.FONT_HERSHEY_SIMPLEX, 2.0,(100, 200, 200), 5)

            cv2.putText(frame,'"%s"'% biaoji ,(int(d[0]),int(d[1])),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (250, 0, 0), 3)

        print(jiluzhuangtai)
        trackingtime=cv2.getTickCount()
        print("tracking时间",(trackingtime-detectiontime)/frquency)
        tracktime+=(trackingtime-detectiontime)/frquency

    if len(sfliterbox)== 1:
        pass#cv2.rectangle(frame, (sfliterbox[0][0], sfliterbox[0][1]), (sfliterbox[0][0] + sfliterbox[0][2], sfliterbox[0][1] + sfliterbox[0][3]), (0, 255, 0), 2)
    if len(sfliterbox)==0:
        trackers = mot_tracker.update(trackers)
        cv2.putText(frame, "未发现可疑目标！", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)



    #做多线程
        # if total_frames%5==0:
        #     t1 = threading.Thread(target=panju, args=(roi,))
        #     t1.start()
        #     t1.join()

    print("      ")

    cv2.imshow('Frame', frame)

    #esc键退出
    if cv2.waitKey(5) == 27 or cv2.waitKey(5) == ord('q'):
        print('exit!\n')
        break
    total_frames+=1
    #cycle_time = time.time() - sstart_time
    cycle_time=(cv2.getTickCount()-start_time)/frquency
    print("一帧时间",cycle_time)
    total_time += cycle_time

print("Total Tracking took: %.3f for %d frames or %.1f FPS" % (total_time, total_frames, total_frames / total_time))
print("平均颜色模型时间",colortime/total_frames)
print("平均追踪时间",tracktime/total_frames)
print("平均判断时间",classfictime/classfictcount)
cap.release()
cv2.destroyAllWindows()


