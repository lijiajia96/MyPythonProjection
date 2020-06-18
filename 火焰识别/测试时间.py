
import torch
from torchvision import transforms
import cv2
from PIL import Image
net = torch.load('D:/zhaopro/fire/modelresnet_fullsize_rgb.pkl')
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
train_transformer_ImageNet = transforms.Compose([
    transforms.RandomResizedCrop(300),
    #transforms.Grayscale(1),
    #transforms.ColorJitter(contrast=(2,3)),
    transforms.ToTensor(),
    normalize
])
def classification(frame):
    imm = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    frame=train_transformer_ImageNet(imm)
    imm2 = torch.unsqueeze(frame, dim=0).float()
    output1 = net(imm2)
    _, predicted = torch.max(output1.data, 1)
    return predicted
cap = cv2.VideoCapture(r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\car3.mp4")
frequency=cv2.getTickFrequency()
countframe=0
cb=cv2.getTickCount()
while (1):
    (ret, frame) = cap.read()
    #a=cv2.getTickCount()
    #resnet1=classification(frame)
    #b=cv2.getTickCount()
    countframe+=1
    cv2.imshow("aaa",frame)
    #print("时间",(b-a)/frequency,resnet1)
ca=cv2.getTickCount()

print(((ca-cb)/frequency)/countframe)