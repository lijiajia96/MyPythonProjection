import cv2
import numpy as np
import time
import threading
from datetime import datetime

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

path = r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\wuchuli\1"   #图像读取地址
#火改为1，非火改为0

caitup = r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\colorcaijieguo\firedidi"  # 图像保存地址
heibaitup=r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\heibaicaijieguo\no_firedidi"
huidutup=r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\huiducaijieguo\firedidi"

filelist = os.listdir(path)  # 打开对应的文件夹
total_num = len(filelist)  #得到文件夹中图像的个数



#设定红色阈值黄色阈值蓝色的阈值绿色阈值，HSV空间
hsv_fire_low1=np.array([5,128,205])
hsv_fire_high1=np.array([33,255,255])

rgb_fire_low1=np.array([200,50,0])
rgb_fire_high1=np.array([255,255,125])

hsv_fire_low2=np.array([23,0,240])
hsv_fire_high2=np.array([40,128,255])

rgb_fire_low2=np.array([230,230,125])
rgb_fire_high2=np.array([255,255,255])

#frame=cv2.imread(r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\Fire images\913_0.jpg")


for jpgname in filelist:
    frame = cv2.imread(path+"/"+jpgname)
    blur = cv2.GaussianBlur(frame,(7,7),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    rgb=cv2.cvtColor(blur,cv2.COLOR_BGR2RGB)
    hsv_mask1 = cv2.inRange(hsv, hsv_fire_low1, hsv_fire_high1)
    rgb_mask1=cv2.inRange(rgb, rgb_fire_low1, rgb_fire_high1)
    hsv_mask2 = cv2.inRange(hsv, hsv_fire_low2, hsv_fire_high2)
    rgb_mask2=cv2.inRange(rgb, rgb_fire_low2, rgb_fire_high2)

    mask1=hsv_mask1+rgb_mask1
    mask2=hsv_mask2+rgb_mask2

    #masknew=mask1+mask2
    masknew = mask1

    # cv2.imshow("原图",frame)
    # cv2.imshow("1",mask1)
    # cv2.imshow("2",mask2)
    # cv2.imshow("3",masknew)

    #自适应图像大小的阈值
    a,b=masknew.shape
    min_thresh = 0.005*a*b
    max_thresh = 0.75*a*0.75*b
    sthord=0.0625*a*b    #合并区域的距离阈值


    output = cv2.connectedComponentsWithStats(masknew,8, cv2.CV_32S)
    contlist=[]
    for i in range(output[0]):
        jj = []
        if output[2][i][4] >= min_thresh and output[2][i][4] <= max_thresh:
            # cv2.rectangle(frame, (output[2][i][0], output[2][i][1]), (output[2][i][0] + output[2][i][2], output[2][i][1] + output[2][i][3]), (0, 255, 0), 2)
            jj = list(output[2][i])
            jj.append(list(output[3][i]))
            jj.append(i)
            # jj=[x0, y0, width, height, area,centroids,i]
            contlist.append(jj)
            # print(jj)
    if len(contlist)>=1:
        listance = []
        maxte=[]
        currentwidow=[]#[[x,y,w,h,id],[]]
        for i in range(0,len(contlist)):
            j = i
            while j + 1 < len(contlist):
                d =np.abs(int(contlist[i][5][0])-int(contlist[j+1][5][0]))+ np.abs(int(contlist[i][5][1])-int(contlist[j+1][5][1]))
                #print(d)
                if d<sthord:   #j距离阈值
                    #判断直方图相似度
                    aa=frame[contlist[i][1]:contlist[i][1]+contlist[i][3],contlist[i][0]:contlist[i][0]+contlist[i][2]]
                    bb=frame[contlist[j+1][1]:contlist[j+1][1]+contlist[j+1][3],contlist[j+1][0]:contlist[j+1][0]+contlist[j+1][2]]
                    histaa = cv2.calcHist(aa, [0], None, [100], [0, 255])
                    histbb = cv2.calcHist(bb, [0], None, [100], [0, 255])

                    #print(histaa.shape,histbb.shape)
                    dist = np.linalg.norm(histaa/(contlist[i][3]*contlist[i][2]) - histbb/(contlist[j+1][3]*contlist[j+1][2]))

                    print(dist)
                    if dist<0.1:
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
    #print(contlist)
    i=0
    filename, extension =os.path.splitext(jpgname)
    for kuang in contlist:
        x0=kuang[0]
        y0=kuang[1]
        x1=kuang[0]+kuang[2]
        y1=kuang[1]+kuang[3]
        areas=kuang[2]*kuang[3]
        if areas>6000:
            caitu=frame[y0:y1,x0:x1]
            #cv2.imwrite(caitup+"/"+filename+str(i)+extension, caitu)

            heibaitu=masknew[y0:y1,x0:x1]
            #cv2.imwrite(heibaitup+"/"+filename+str(i)+extension, heibaitu)

            cv2.imwrite(huidutup + "/" + filename + str(i) + extension, caitu)

        i+=1
cv2.waitKey(0)




