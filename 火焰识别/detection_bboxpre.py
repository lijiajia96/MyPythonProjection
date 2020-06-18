import cv2
import numpy as np
import time
import threading
from PIL import Image
from datetime import datetime
import torch
#from CNN2 import LeNet
import torch.nn as nn
from torchvision import transforms

start=time.time()

import os.path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io
from sklearn.utils.linear_assignment_ import linear_assignment
import glob

#pip install C:\Users\miaojia.li\Desktop\tensorflow-2.1.0-cp37-cp37m-win_amd64.whl
#pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# H: ps=opencv*2
# S: ps=opencv*0.392
# V: ps=opencv*0.392

def panju(image):
    cv2.imshow('tagimage', image)
    dt = datetime.now()
    a=dt.strftime('%H%M%S')
    cv2.imwrite("C:/"+str(a)+".png",image)
    print("写入成功")
    #cv2.waitKey()


class LeNet(nn.Module):
    def __init__(self):
        # Net继承nn.Module类，这里初始化调用Module中的一些方法和属性
        nn.Module.__init__(self)
        # 定义特征工程网络层，用于从输入数据中进行抽象提取特征
        self.feature_engineering = nn.Sequential(
            nn.Conv2d(in_channels=3,
                      out_channels=6,
                      kernel_size=5),
            # kernel_size=2, stride=2，正好可以将图片长宽尺寸缩小为原来的一半
            nn.MaxPool2d(kernel_size=2,
                         stride=2),
            nn.Conv2d(in_channels=6,
                      out_channels=16,
                      kernel_size=5),
            nn.MaxPool2d(kernel_size=2,
                         stride=2),
            nn.Conv2d(in_channels=16,
                      out_channels=32,
                      kernel_size=5),
            nn.MaxPool2d(kernel_size=2,
                         stride=2),
            nn.ReLU()

        )

        # 分类器层，将self.feature_engineering中的输出的数据进行拟合
        self.classifier = nn.Sequential(
            nn.Linear(in_features=32 * 24 * 24,
                      out_features=1000),

            nn.Linear(in_features=1000,
                      out_features=100),

            nn.Linear(in_features=100,
                      out_features=2),

        )

    def forward(self, x):
        # 在Net中改写nn.Module中的forward方法。
        # 这里定义的forward不是调用，我们可以理解成数据流的方向，给net输入数据inpput会按照forward提示的流程进行处理和操作并输出数据
        x = self.feature_engineering(x)
        print(x.shape)
        x = x.view(-1, 32 * 24 * 24)
        x = self.classifier(x)
        return x



def classification(frame):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    transformer_Image = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        normalize
    ])
    imm = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    imm1=transformer_Image(imm)
    imm2=torch.unsqueeze(imm1, dim=0).float()
    output=model(imm2)
    _, predicted = torch.max(output.data, 1)
    print(predicted)
    return predicted
#mot_tracker = sortMOT.Sort()
currentwidow=[]

#设定红色阈值黄色阈值蓝色的阈值绿色阈值，HSV空间
hsv_fire_low1=np.array([5,128,205])
hsv_fire_high1=np.array([33,255,255])

rgb_fire_low1=np.array([200,50,0])
rgb_fire_high1=np.array([255,255,125])

hsv_fire_low2=np.array([23,0,240])
hsv_fire_high2=np.array([40,128,255])

rgb_fire_low2=np.array([230,230,125])
rgb_fire_high2=np.array([255,255,255])

frame=cv2.imread(r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\wuchuli\1\1 (4).jpg")

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
hsv_mask1 = cv2.inRange(hsv, hsv_fire_low1, hsv_fire_high1)
rgb_mask1=cv2.inRange(rgb, rgb_fire_low1, rgb_fire_high1)
# hsv_mask2 = cv2.inRange(hsv, hsv_fire_low2, hsv_fire_high2)
# rgb_mask2=cv2.inRange(rgb, rgb_fire_low2, rgb_fire_high2)


# cv2.getCPUTickCount()
# cv2.getTickFrequency()
# cv2.getTickCount()
#
# 总次数/一秒内重复的次数 = 时间(s)
# 1000 *总次数/一秒内重复的次数= 时间(ms)
# 这个逻辑很清晰，没什么问题，但是这里有一个小坑，那就是C版本的cvGetTickFrequency()函数和C++版本的getTickFrequency()的单位不一样，前者以ms计算频率，后者以s为单位计算频率，所以如果使用C版本的cvGetTickFrequency()计算时间的话，应该是：
# 总次数/一秒内重复的次数*1000 = 时间(ms)
# 总次数/一秒内重复的次数*1000000 = 时间(s


mask1=hsv_mask1+rgb_mask1
#mask2=hsv_mask2+rgb_mask2

# cv2.imshow("原图",frame)
# cv2.imshow("1",mask1)
# cv2.imshow("2",mask2)

model = torch.load('D:/zhaopro/fire/model.pkl')
end1=time.time()
a=classification(frame)


end=time.time()
print('Running time  Seconds',(end1-start),(end-end1))
cv2.waitKey(0)

#指定写视频的格式, I420-avi, MJPG-mp4
# fps=25
# size=640,480
# out_frame = cv2.VideoWriter('c://color_track.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
# out_hsv = cv2.VideoWriter('c://color_detect_hsv.avi', cv2.VideoWriter_fourcc(*'MP42'), fps, size)
# out_mask = cv2.VideoWriter('c://color_detect_mask.avi', cv2.VideoWriter_fourcc(*'MP42'), fps, size)

# cap = cv2.VideoCapture("F:/python/学习练习/fire/20191120_162459.mp4")
#
# total_time = 0.0
# total_frames = 0
#
# while (1):
#     (ret, frame) = cap.read()
#     if not ret:
#         print ('No Camera\n')
#         break
#     start_time = time.time()
#     #转到绿色的HSV空间
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     #根据阈值构建蒙版掩膜
#     #mask = cv2.inRange(hsv, lower_red, upper_red)
#     #mask = cv2.inRange(hsv, lower_blue, upper_blue)
#
#     mask_hsv = cv2.inRange(hsv,hsv_fire_low, hsv_fire_high)
#
#
#     # mask_red = cv2.erode(mask_red, None, iterations=2)
#     # mask_red = cv2.dilate(mask_red, None, iterations=3)
#
#     #mask = mask_green+mask_red+mask_yellow
#     mask = mask_hsv
#     #最大面积和最小面积阈值
#     min_thresh = 1000
#     max_thresh = 60000
#     output = cv2.connectedComponentsWithStats(mask,8, cv2.CV_32S)
#     # _, labels, stats, centroids.
#     # stats 是bounding box的信息，N*5的矩阵，行对应每个label，五列分别为[x0, y0, width, height, area]
#     # centroids 是每个域的质心坐标
#     contlist=[]
#     lastwindow=currentwidow#保存一下上一帧的框框
#     print("上帧追踪框参数",lastwindow)
#
#     for i in range(output[0]):
#         jj=[]
#         if output[2][i][4] >= min_thresh and output[2][i][4] <= max_thresh:
#             #cv2.rectangle(frame, (output[2][i][0], output[2][i][1]), (output[2][i][0] + output[2][i][2], output[2][i][1] + output[2][i][3]), (0, 255, 0), 2)
#             jj=list(output[2][i])
#             jj.append(list(output[3][i]))
#             jj.append(i)
#             #jj=[x0, y0, width, height, area,centroids,i]
#             contlist.append(jj)
#             #print(jj)
#     # contlist=[[x0, y0, width, height, area,centroids,i],[x0, y0, width, height, area,centroids,i]]
#     if len(contlist)>=1:
#         listance = []
#         maxte=[]
#         currentwidow=[]#[[x,y,w,h,id],[]]
#         for i in range(0,len(contlist)):
#             j = i
#             while j + 1 < len(contlist):
#                 # print(contlist)
#                 # print(contlist[i])
#                 # print(contlist[i][5][0])
#                 d =np.abs(int(contlist[i][5][0])-int(contlist[j+1][5][0]))+ np.abs(int(contlist[i][5][1])-int(contlist[j+1][5][1]))
#                 #print(d)
#                 if d<300:   #j距离阈值
#                     #找出两个区域合并后矩形的参数
#                     x = min([contlist[i][0], contlist[j + 1][0]])
#                     y = min([contlist[i][1], contlist[j + 1][1]])
#                     w = contlist[i][2]+contlist[j + 1][2]
#                     h = contlist[i][3]+contlist[j + 1][3]
#                     # 把两个区域的的面积 全放到 后面的元素上
#                     contlist[j + 1][0] = x
#                     contlist[j + 1][1] = y
#                     contlist[j + 1][2] = w
#                     contlist[j + 1][3] = h
#                     contlist[j + 1][6] = contlist[i][6]
#                     contlist.remove(contlist[i])
#
#                 j=j+1
#
#         # 把conlist中的每个框的id变成从0开始
#         for i in range(len(contlist)):
#             contlist[i][6]=i
#             guodu=contlist[i][:4]
#             guodu.append(contlist[i][6])
#             guodu=np.array(guodu)
#             currentwidow.append(guodu)
#
#         print("本帧追踪框参数",currentwidow)
#         detection=np.array(currentwidow)
#         detection[:, 2:4] += detection[:, 0:2]
#         print(detection)
#         trackers = mot_tracker.update(detection)
#
#         trackers=trackers.astype(int)
#
#         for d in trackers:
#             print (type(int(d[4])))
#             biaoji=str(d[4])
#             cv2.rectangle(frame,(int(d[0]), int(d[1])), (int(d[2]),int(d[3])),(0, 255, 0), 2)
#             cv2.putText(frame,'"%s"'% biaoji ,(int(d[0]),int(d[1])),cv2.FONT_HERSHEY_SIMPLEX, 2.0, (100, 200, 200), 5)
#             # with open("zuizong.txt", "w") as outfile:
#             #     print('%d,%d,%d,%d,%d,%d' % (total_frames,int(d[4]),int(d[0]),int(d[1]),int(d[2])-int(d[0]),int(d[3])-int(d[1])),file=outfile)
#
#
#     if len(contlist)== 1:
#         cv2.rectangle(frame, (contlist[0][0], contlist[0][1]),(contlist[0][0] + contlist[0][2], contlist[0][1] + contlist[0][3]), (0, 255, 0), 2)
#     if len(contlist)==0:
#         cv2.putText(frame, "未发现可疑目标！", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
#
#
#
#     #做多线程
#         # if total_frames%5==0:
#         #     t1 = threading.Thread(target=panju, args=(roi,))
#         #     t1.start()
#         #     t1.join()
#
#     print("      ")
#
#     cv2.imshow('Frame', frame)
#
#     #esc键退出
#     if cv2.waitKey(5) == 27 or cv2.waitKey(5) == ord('q'):
#         print('exit!\n')
#         break
#     total_frames+=1
#     cycle_time = time.time() - start_time
#     total_time += cycle_time
#
# print("Total Tracking took: %.3f for %d frames or %.1f FPS" % (total_time, total_frames, total_frames / total_time))
#
# cap.release()
# cv2.destroyAllWindows()


