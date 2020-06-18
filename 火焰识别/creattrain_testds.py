from torchvision.datasets import ImageFolder
from PIL import Image
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms



#normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
#normalize = transforms.Normalize(mean=[0.485], std=[0.229])
train_transformer_ImageNet = transforms.Compose([
    transforms.Resize(120),
    transforms.RandomResizedCrop(112),
    #transforms.RandomHorizontalFlip(),
    transforms.Grayscale(1),
    #transforms.ColorJitter(contrast=(2,3)),

    transforms.ToTensor(),
    #normalize
])

val_transformer_ImageNet = transforms.Compose([
    transforms.Resize(112),
    transforms.Grayscale(1),
    #transforms.ColorJitter(contrast=(2, 3)),
    transforms.ToTensor(),
    #normalize
])


class MyDataset(Dataset):
    def __init__(self, filenames, labels, transform):
        self.filenames = filenames
        self.labels = labels
        self.transform = transform

    def __len__(self):  # 因为漏了这行代码，花了一个多小时解决问题
        return len(self.filenames)

    def __getitem__(self, idx):
        #image = Image.open(self.filenames[idx]).convert('RGB')
        image = Image.open(self.filenames[idx])
        #print(image.shape)
        image = self.transform(image)
        return image, self.labels[idx]


def fetch_dataloaders(data_dir, ratio, batchsize=32):
    """ the sum of ratio must equal to 1"""
    dataset = ImageFolder(data_dir)
    character = [[] for i in range(len(dataset.classes))]
    jj=0
    print(dataset.class_to_idx)
    for x, y in dataset.samples:  # 将数据按类标存放
        character[y].append(x)
    train_inputs, val_inputs, test_inputs = [], [], []
    train_labels, val_labels, test_labels = [], [], []
    for i, data in enumerate(character):
        num_sample_train = int(len(data) * ratio[0])
        num_sample_val = int(len(data) * ratio[1])
        num_val_index = num_sample_train + num_sample_val

        for x in data[:num_sample_train]:
            with open('D:/zhaopro/fire/picture_and_order_train.txt', 'a') as f:
                f.write("第{}个图片: {}\r\n".format(jj, str(x)))
            jj+=1
            train_inputs.append(str(x))
            train_labels.append(i)
        for x in data[num_sample_train:num_val_index]:
            val_inputs.append(str(x))
            val_labels.append(i)
        for x in data[num_val_index:]:
            test_inputs.append(str(x))
            test_labels.append(i)

    train_dataloader = DataLoader(MyDataset(train_inputs, train_labels, train_transformer_ImageNet), batch_size=batchsize, drop_last=True, shuffle=True)
    # val_dataloader = DataLoader(MyDataset(val_inputs, val_labels, val_transformer_ImageNet), batch_size=1, shuffle=True)
    # test_dataloader = DataLoader(MyDataset(test_inputs, test_labels, val_transformer_ImageNet), batch_size=1, shuffle=True)

    loader = {}
    #loader['train'] = train_dataloader
    # loader['val'] = val_dataloader
    # loader['test'] = test_dataloader

    return train_dataloader
#
# data_dir =r"C:\Users\miaojia.li\Documents\WeChat Files\lijia1000\FileStorage\File\2020-02\fire_dataset\colorcaijieguo"
# # #
# loader = fetch_dataloaders(data_dir, [0.6, 0.2, 0.2], batchsize=1)
# print(len(loader['val']))
# #for x, y in loader['train']:

def fetch_test(data_dir, ratio, batchsize=32):
    """ the sum of ratio must equal to 1"""
    dataset = ImageFolder(data_dir)
    character = [[] for i in range(len(dataset.classes))]

    print(dataset.class_to_idx)
    for x, y in dataset.samples:  # 将数据按类标存放
        character[y].append(x)
    test_inputs = []
    test_labels = []
    jj = 0
    for i, data in enumerate(character):
        num_sample_test = int(len(data) * ratio[0])

        for x in data[:num_sample_test]:
            with open('D:/zhaopro/fire/picture_and_order.txt', 'a') as f:
                f.write("第{}个图片: {}\r\n".format(jj, str(x)))
            jj+=1
            test_inputs.append(str(x))
            test_labels.append(i)


    #train_dataloader = DataLoader(MyDataset(train_inputs, train_labels, train_transformer_ImageNet), batch_size=batchsize, drop_last=True, shuffle=True)
    # val_dataloader = DataLoader(MyDataset(val_inputs, val_labels, val_transformer_ImageNet), batch_size=1, shuffle=True)
    test_dataloader = DataLoader(MyDataset(test_inputs, test_labels, val_transformer_ImageNet), batch_size=1, shuffle=False)
    return test_dataloader