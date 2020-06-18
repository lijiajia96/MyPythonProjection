import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread(r'C:\Users\miaojia.li\Desktop\111\11 (36).jpg',0)
img2 = cv2.imread(r'C:\Users\miaojia.li\Desktop\111\111 (36).jpg',0)
img3 = cv2.imread(r'C:\Users\miaojia.li\Desktop\111\1111(36).jpg',0)
# mask1 = np.zeros(img.shape[:2],np.uint8)
# mask1[400:660,150:430] = 255
# mask2 = np.zeros(img.shape[:2],np.uint8)
# mask2[100:550,0:180] = 255
# mask3 = np.zeros(img.shape[:2],np.uint8)
# mask3[100:300,180:450] = 255

# masked_img1 = cv2.bitwise_and(img, img,mask = mask1)
# masked_img2 = cv2.bitwise_and(img, img,mask = mask2)
# masked_img3 = cv2.bitwise_and(img, img,mask = mask3)
s1=img1.shape[0]*img1.shape[1]
s2=img2.shape[0]*img2.shape[1]
s3=img3.shape[0]*img3.shape[1]

hist_mask1,bins1=np.histogram(img1.ravel(),32,[0,256])
hist_mask2,bins2=np.histogram(img2.ravel(),32,[0,256])
hist_mask3,bins3=np.histogram(img3.ravel(),32,[0,256])
hist_mask11 = cv2.calcHist(img1,  [0], None, [32], [0,256])/float(s1)
# hist_mask2 = cv2.calcHist(img2, [0], None, [32], [0,256])/float(s2)
# hist_mask3 = cv2.calcHist(img3, [0], None, [32], [0,256])/float(s3)
print(hist_mask11.shape)
hist_mask1=hist_mask1/float(s1)
hist_mask2=hist_mask2/float(s2)
hist_mask3=hist_mask3/float(s3)

hist_mask1 = hist_mask1.astype(np.float32)
hist_mask2 = hist_mask2.astype(np.float32)
hist_mask3 = hist_mask3.astype(np.float32)

hist_mask1=hist_mask1.reshape(-1,1)
hist_mask2=hist_mask2.reshape(-1,1)
hist_mask3=hist_mask3.reshape(-1,1)
print(hist_mask1.shape,hist_mask2.shape,hist_mask3.shape)
dist12=cv2.compareHist(hist_mask1, hist_mask2, cv2.HISTCMP_CORREL)
dist13=cv2.compareHist(hist_mask1, hist_mask3, cv2.HISTCMP_CORREL)
dist23=cv2.compareHist(hist_mask2, hist_mask3, cv2.HISTCMP_CORREL)
#
print(dist12,dist13,dist23)
cv2.imshow("1",img1)
cv2.imshow("2",img2)
cv2.imshow("3",img3)


xxx1=np.arange(0,33,1)
xxx11=np.arange(0,257,8)
xxx=["0","","","","","","","","64","","","","","","","","128","","","","","","","","192","","","","","","","","256"]


plt.subplot(131),plt.plot(hist_mask1)
plt.xticks(xxx1,(xxx))
plt.subplot(132),plt.plot(hist_mask2)
plt.yticks(())
plt.xticks(xxx1,(xxx))
plt.subplot(133),plt.plot(hist_mask3)
plt.yticks(())
plt.xticks(xxx1,(xxx))
plt.show()
cv2.waitKey(0)