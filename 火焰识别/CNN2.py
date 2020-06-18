import torchvision as tv
import torchvision.transforms as transforms
from torchvision.transforms import ToPILImage
import torch as t
import torch
import torch.nn as nn
from torch import optim
import creattrain_testds
from torch.utils.tensorboard import SummaryWriter
from torchvision.utils import make_grid
# import torchvision.models as models
# resnet101 = models.resnet18()
# alexnet = models.alexnet()
# squeezenet = models.squeezenet1_0()
# densenet = models.densenet_161()


#y=ceil((x+2p-k-(k-1)*(d-1)+1)/s)
#wo = (w - F + 2*P)/S +1
class LeNet(nn.Module):
    def __init__(self):
        # Net继承nn.Module类，这里初始化调用Module中的一些方法和属性
        nn.Module.__init__(self)
        # 定义特征工程网络层，用于从输入数据中进行抽象提取特征
        self.feature_engineering = nn.Sequential(
            nn.GroupNorm(1, 1),
            nn.Conv2d(in_channels=1,
                      out_channels=3,
                      kernel_size=5),
            # kernel_size=2, stride=2，正好可以将图片长宽尺寸缩小为原来的一半
            nn.BatchNorm2d(3),
            nn.ReLU(),
            nn.Conv2d(in_channels=3,
                      out_channels=9,
                      kernel_size=5),
            # kernel_size=2, stride=2，正好可以将图片长宽尺寸缩小为原来的一半
            nn.BatchNorm2d(9),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,
                         stride=2),

            nn.Conv2d(in_channels=9,
                      out_channels=27,
                      kernel_size=3),

            nn.ReLU(),
            nn.Conv2d(in_channels=27,
                      out_channels=54,
                      kernel_size=3),

            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,
                         stride=2),

            nn.Conv2d(in_channels=54,
                      out_channels=108,
                      kernel_size=3),

            nn.ReLU(),
            # nn.MaxPool2d(kernel_size=2,
            #              stride=2),

            nn.Conv2d(in_channels=108,
                      out_channels=216,
                      kernel_size=3),

            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,
                         stride=2),
            #nn.AdaptiveAvgPool2d(5),

        )

        # 分类器层，将self.feature_engineering中的输出的数据进行拟合
        self.classifier = nn.Sequential(
            nn.Linear(in_features=216 * 28 * 28,
                      out_features=1000),
            nn.ReLU(),
            nn.Dropout(0.5),
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
        x = x.view(-1, 216 *5 *5)
        x = self.classifier(x)
        return x
def correct_rate(net, testloader):
    correct = 0
    total = 0
    correcttp=0
    correctfn=0
    correctfp=0
    correcttn=0
    i=0
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = t.max(outputs.data, 1)
        print(predicted)
        total += labels.size(0)
        #correcttp += (predicted == labels).sum()
        if labels!=predicted:
            print("第i幅图错误",i)
        if labels==0:
            if predicted==0:
                correcttp +=1
            if predicted==1:
                correctfp += 1
        if labels==1:
            if predicted==1:
                correcttn += 1
            if predicted == 0:
                correctfn +=1
        i+=1
    print("tp:",correcttp)
    print("fn:",correctfn)
    print("tn:",correcttn)
    print("fp",correctfp)


    print("精确率:",correcttp/(correcttp+correctfp))
    print("召回率:",correcttp/(correcttp+correctfn))
    print("准确率：",(correcttp+correcttn)/total)
    return 100 * correct / total



data_dir =r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\colorcaijieguo"
test_dir=r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\test"
#未经裁剪的原图"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\wuchuli"
#裁剪后的彩图：C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\colorcaijieguo
#裁剪后的黑白图：C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\heibaicaijieguo

loader = creattrain_testds.fetch_dataloaders(data_dir, [1, 0.2, 0.1], batchsize=32)
testdata=creattrain_testds.fetch_test(test_dir, [1, 0.2, 0.1], batchsize=1)

print(len(loader))
print(len(testdata))


#writer.add_image('feature_map', make_grid([feature_map1, feature_map2, fetare_map3], padding=20, normalize=True, scale_each=True, pad_value=1), curr_step)
#net = LeNet()
net = torch.load('D:/zhaopro/fire/modelresnetquanchicun.pkl')
#net=tv.models.vgg16(pretrained=False)
#net=tv.models.resnet18()
#net=tv.models.SqueezeNet()
#net=tv.models.shufflenet_v2_x0_5()

#a=correct_rate(net,loader)
criterion = nn.CrossEntropyLoss()
#criterion = nn.BCEWithLogitsLoss()

#optimizer = optim.SGD(params=net.parameters(),lr=0.0001)
optimizer= optim.Adam(params=net.parameters(), lr=0.001)

epochs = 500
average_loss_series = []
print("?????????")
for epoch in range(epochs):
    running_loss = 0.0
    for i, data in enumerate(loader):
        inputs, labels = data
        # inputs, labels = Variable(inputs), Variable(labels)

        # 梯度清零
        optimizer.zero_grad()
        # forward+backward
        outputs = net(inputs)

        # 对比预测结果和labels，计算loss
        loss = criterion(outputs, labels)
        #print(loss)
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()
        # 打印log
        running_loss += loss.item()
        if i % 10 == 9:  # 每20个batch打印一次训练状态
            average_loss = running_loss /10
            print("[{0},{1}] loss:  {2}".format(epoch + 1, i + 1, average_loss))
            average_loss_series.append(average_loss)
            running_loss = 0.0
    if epoch% 500 == 499:
        torch.save(net, 'D:/zhaopro/fire/modelshuffnet_500.pkl')
import matplotlib.pyplot as plt

x = range(0, len(average_loss_series))
plt.figure()
plt.plot(x, average_loss_series)

#查看准确率d

torch.save(net, 'D:/zhaopro/fire/modelresnetshufnet.pkl')
correct = correct_rate(net, testdata)
print('10000张测试集中准确率为： {}%'.format(correct))


plt.show()
