# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 16:00:12 2020

@author: 
"""

#%%
#库文件加载
#from sklearn.datasets import load_iris
import numpy as np
import math
from collections import Counter
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import  OneHotEncoder
#%%
#函数定义
class decisionnode:
    def __init__(self, d=None, thre=None, results=None, NH=None, lb=None, rb=None, max_label=None):
        self.d = d   # d表示维度
        self.thre = thre  # thre表示二分时的比较值，将样本集分为2类
        self.results = results  # 最后的叶节点代表的类别
        self.NH = NH  # 存储各节点的样本量与经验熵的乘积，便于剪枝时使用
        self.lb = lb  # desision node,对应于样本在d维的数据小于thre时，树上相对于当前节点的子树上的节点
        self.rb = rb  # desision node,对应于样本在d维的数据大于thre时，树上相对于当前节点的子树上的节点
        self.max_label = max_label  # 记录当前节点包含的label中同类最多的label


def entropy(y):
    '''
    计算信息熵，y为labels
    '''

    if y.size > 1:

        category = list(set(y))
    else:

        category = [y.item()]
        y = [y.item()]

    ent = 0

    for label in category:
        p = len([label_ for label_ in y if label_ == label]) / len(y)
        ent += -p * math.log(p, 2)

    return ent


def Gini(y):
    '''
    计算基尼指数，y为labels
    '''
    category = list(set(y))
    gini = 1

    for label in category:
        p = len([label_ for label_ in y if label_ == label]) / len(y)
        gini += -p * p

    return gini


def GainEnt_max(X, y, d):
    '''
    计算选择属性attr的最大信息增益，X为样本集,y为label，d为一个维度，type为int
    '''
    ent_X = entropy(y)
    X_attr = X[:, d]
    X_attr = list(set(X_attr))
    X_attr = sorted(X_attr)
    Gain = 0
    thre = 0

    for i in range(len(X_attr) - 1):
        thre_temp = (X_attr[i] + X_attr[i + 1]) / 2
        y_small_index = [i_arg for i_arg in range(
            len(X[:, d])) if X[i_arg, d] <= thre_temp]
        y_big_index = [i_arg for i_arg in range(
            len(X[:, d])) if X[i_arg, d] > thre_temp]
        y_small = y[y_small_index]
        y_big = y[y_big_index]

        Gain_temp = ent_X - (len(y_small) / len(y)) * \
            entropy(y_small) - (len(y_big) / len(y)) * entropy(y_big)
        '''
        intrinsic_value = -(len(y_small) / len(y)) * math.log(len(y_small) /
                                                              len(y), 2) - (len(y_big) / len(y)) * math.log(len(y_big) / len(y), 2)
        Gain_temp = Gain_temp / intrinsic_value
        '''
        # print(Gain_temp)
        if Gain < Gain_temp:
            Gain = Gain_temp
            thre = thre_temp
    return Gain, thre


def Gini_index_min(X, y, d):
    '''
    计算选择属性attr的最小基尼指数，X为样本集,y为label，d为一个维度，type为int
    '''

    X = X.reshape(-1, len(X.T))
    X_attr = X[:, d]
    X_attr = list(set(X_attr))
    X_attr = sorted(X_attr)
    Gini_index = 1
    thre = 0

    for i in range(len(X_attr) - 1):
        thre_temp = (X_attr[i] + X_attr[i + 1]) / 2
        y_small_index = [i_arg for i_arg in range(
            len(X[:, d])) if X[i_arg, d] <= thre_temp]

        y_big_index = [i_arg for i_arg in range(
            len(X[:, d])) if X[i_arg, d] > thre_temp]
        y_small = y[y_small_index]
        y_big = y[y_big_index]

        Gini_index_temp = (len(y_small) / len(y)) * \
            Gini(y_small) + (len(y_big) / len(y)) * Gini(y_big)
        if Gini_index > Gini_index_temp:
            Gini_index = Gini_index_temp
            thre = thre_temp
    return Gini_index, thre


def attribute_based_on_GainEnt(X, y):
    '''
    基于信息增益选择最优属性，X为样本集，y为label
    '''
    D = np.arange(len(X[0]))
    Gain_max = 0
    thre_ = 0
    d_ = 0
    for d in D:
        Gain, thre = GainEnt_max(X, y, d)
        if Gain_max < Gain:
            Gain_max = Gain
            thre_ = thre
            d_ = d  # 维度标号

    return Gain_max, thre_, d_


def attribute_based_on_Giniindex(X, y):
    '''
    基于信息增益选择最优属性，X为样本集，y为label
    '''
    D = np.arange(len(X.T))
    Gini_Index_Min = 1
    thre_ = 0
    d_ = 0
    for d in D:
        Gini_index, thre = Gini_index_min(X, y, d)
        if Gini_Index_Min > Gini_index:
            Gini_Index_Min = Gini_index
            thre_ = thre
            d_ = d  # 维度标号

    return Gini_Index_Min, thre_, d_


def devide_group(X, y, thre, d):
    '''
    按照维度d下阈值为thre分为两类并返回
    '''
    X_in_d = X[:, d]
    x_small_index = [i_arg for i_arg in range(
        len(X[:, d])) if X[i_arg, d] <= thre]
    x_big_index = [i_arg for i_arg in range(
        len(X[:, d])) if X[i_arg, d] > thre]

    X_small = X[x_small_index]
    y_small = y[x_small_index]
    X_big = X[x_big_index]
    y_big = y[x_big_index]
    return X_small, y_small, X_big, y_big


def NtHt(y):
    '''
    计算经验熵与样本数的乘积，用来剪枝，y为labels
    '''
    ent = entropy(y)
    print('ent={},y_len={},all={}'.format(ent, len(y), ent * len(y)))
    return ent * len(y)


def maxlabel(y):
    label_ = Counter(y).most_common(1)
    return label_[0][0]


def buildtree(X, y, method='Gini'):
    '''
    递归的方式构建决策树
    '''
    if y.size > 1:
        if method == 'Gini':
            Gain_max, thre, d = attribute_based_on_Giniindex(X, y)
        elif method == 'GainEnt':
            Gain_max, thre, d = attribute_based_on_GainEnt(X, y)
        if (Gain_max > 0 and method == 'GainEnt') or (Gain_max >= 0 and len(list(set(y))) > 1 and method == 'Gini'):
            X_small, y_small, X_big, y_big = devide_group(X, y, thre, d)
            left_branch = buildtree(X_small, y_small, method=method)
            right_branch = buildtree(X_big, y_big, method=method)
            nh = NtHt(y)
            max_label = maxlabel(y)
            return decisionnode(d=d, thre=thre, NH=nh, lb=left_branch, rb=right_branch, max_label=max_label)
        else:
            nh = NtHt(y)
            max_label = maxlabel(y)
            return decisionnode(results=y[0], NH=nh, max_label=max_label)
    else:
        nh = NtHt(y)
        max_label = maxlabel(y)
        return decisionnode(results=y.item(), NH=nh, max_label=max_label)


def printtree(tree, indent='-', dict_tree={}, direct='L'):
    # 是否是叶节点

    if tree.results != None:
        print(tree.results)

        dict_tree = {direct: str(tree.results)}

    else:
        # 打印判断条件
        Attri = ''
        if tree.d == 0:
            Attri = 'A'
        elif tree.d == 1:
            Attri = 'B'
        elif tree.d == 2:
            Attri = 'C'
        elif tree.d == 3:
            Attri = 'D'
        elif tree.d == 4:
            Attri = 'E'
        else:
            Attri = 'F'
        #print("属性" + str(tree.d) + "<" + str(float("{0:.2f}".format(tree.thre))) + "? ")
        print(Attri  + "<" + str(float("{0:.2f}".format(tree.thre))) + "? ")
        # 打印分支
        print(indent + "Y->",)

        a = printtree(tree.lb, indent=indent + "-", direct='Y')
        aa = a.copy()
        print(indent + "N->",)

        b = printtree(tree.rb, indent=indent + "-", direct='N')
        bb = b.copy()
        aa.update(bb)
        stri = Attri + "<" + str(float("{0:.2f}".format(tree.thre))) + "?"
        if indent != '-':
            dict_tree = {direct: {stri: aa}}
        else:
            dict_tree = {stri: aa}

    return dict_tree


def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.d]
        branch = None

        if v > tree.thre:
            branch = tree.rb
        else:
            branch = tree.lb

        return classify(observation, branch)


def pruning(tree, alpha=0.1):
    if tree.lb.results == None:
        pruning(tree.lb, alpha)
    if tree.rb.results == None:
        pruning(tree.rb, alpha)

    if tree.lb.results != None and tree.rb.results != None:
        before_pruning = tree.lb.NH + tree.rb.NH + 2 * alpha
        after_pruning = tree.NH + alpha
        print('before_pruning={},after_pruning={}'.format(
            before_pruning, after_pruning))
        if after_pruning <= before_pruning:
            print('pruning--{}:{}?'.format(tree.d, tree.thre))
            tree.lb, tree.rb = None, None
            tree.results = tree.max_label

# bins=[0,59,70,80,100]
# score_cat = pd.cut(score_list, bins)

#enc = preprocessing.OneHotEncoder()
def cross_f(zu1,zu2):
    result=[]
    for i in range(len(zu1)):
        #zhuanzhi=zu1[i].T
        jieguo=zu1[i][:,None]*zu2[i]
        jieguo=jieguo.reshape(1,-1)
        result.append(jieguo)
    resnp=np.array(result).squeeze()
    return resnp

#%%
#主程序
if __name__ == '__main__':
    '''
    iris = load_iris()
    X = iris.data
    y = iris.target
    '''
    f=pd.read_csv(r'C:\Users\miaojia.li\Desktop\20180506-change1-unchanged0.csv')
    #names = ['Behavior_Occurences','Indoor_illumination',
             #'Horizontal_irradiance','Outdoor_temperature','Initial_state'])
    #f = pd.get_dummies(f, columns =['Initial state'])
    poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
    enc= OneHotEncoder()

    n = f.shape[1]
    X_data = f.iloc[:, 1:n]  # 使用n-1个特征
    print(X_data)
    y_data = f.iloc[:,0:1]

    edge_1=[0,0.36,0.72,1.08,1.44,101]
    x_1 = pd.cut(X_data['临近遮阳状态'], edge_1,include_lowest=True, labels=False).values
    x_11=enc.fit_transform(x_1.reshape(-1,1)).A

    x_2=X_data['照明状态'].values
    x_22=enc.fit_transform(x_2.reshape(-1,1)).A

    edge_3=[0,300,600,900,1301]
    x_3=pd.cut(X_data['人员位置光照度'], edge_3,include_lowest=True, labels=False).values.reshape(-1, 1)
    x_33= enc.fit_transform(x_3).A

    x_4=X_data['窗户状态'].values
    x_44 = enc.fit_transform(x_4.reshape(-1, 1)).A

    x_5=X_data['空调状态'].values
    x_55 = enc.fit_transform(x_5.reshape(-1, 1)).A

    edge_6=[20, 22, 24, 26, 28, 30, 33]
    x_6= pd.cut(X_data['室内温度'], edge_6,include_lowest=True, labels=False).values
    x_66 = enc.fit_transform(x_6.reshape(-1, 1)).A

    edge_7=[0,200,400,600,800,1000,1201]
    x_7 = pd.cut(X_data['水平面辐照度'], edge_7,include_lowest=True, labels=False).values
    x_77 = enc.fit_transform(x_7.reshape(-1, 1)).A

    edge_8=[15,20,25,30,35,40]
    x_8 = pd.cut(X_data['室外温度'], edge_8,include_lowest=True, labels=False).values
    x_88 = enc.fit_transform(x_8.reshape(-1, 1)).A

    edge_9=[0,50,100,150,200,250,300,350,401]
    x_9 = pd.cut(X_data['南向垂直面辐照度'], edge_9,include_lowest=True, labels=False).values
    x_99 = enc.fit_transform(x_9.reshape(-1, 1)).A

    edge_10=[-15,0,15,30,45,60,75,91]
    x_10 = pd.cut(X_data['高度角'], edge_10,include_lowest=True, labels=False).values
    x_1010 = enc.fit_transform(x_10.reshape(-1, 1)).A

    edge_11=[-115,-55,5,65,126]
    x_111 = pd.cut(X_data['方位角'], edge_11,include_lowest=True, labels=False).values
    print(x_111)
    x_11111 = enc.fit_transform(x_111.reshape(-1, 1)).A
    print(x_11111)


    #高度角+方位角
    crs0=cross_f(x_1010,x_11111)
    #人员光照位置+室内温度
    crs1=cross_f(x_33,x_66)
    #人员光照位置+水平面辐照度
    crs2=cross_f(x_33,x_77)
    #人员光照位置+室外温度
    crs3=cross_f(x_33,x_88)
    #人员关照位置+南向垂直面辐照度
    crs4=cross_f(x_33,x_99)
    #室内温度+水平面辐照度
    crs5=cross_f(x_66,x_77)
    #室内温度+室外温度
    crs6=cross_f(x_66,x_88)
    #室内温度+南向垂直面辐照度
    crs7=cross_f(x_66,x_99)
    #室外温度+水平面辐照度
    crs8=cross_f(x_88,x_77)
    #室外温度+南向垂直面辐照度
    crs9=cross_f(x_88,x_99)
    print(crs0.shape,crs1.shape,crs2.shape,crs3.shape,crs4.shape,crs5.shape,crs6.shape,crs7.shape,crs8.shape,crs9.shape)

    jiaochashujju=np.concatenate((crs0,crs1,crs2,crs3,crs4,crs5,crs6,crs7,crs8,crs9), axis=1)
    saveit=pd.DataFrame(jiaochashujju)
    saveit.to_csv(r'C:\Users\miaojia.li\Desktop\jiaochajieguo1.csv')



    newinput=np.concatenate((x_11,x_22,x_33,x_44,x_55,x_66,x_77,x_88,x_99), axis=1)
    print(newinput)
    print(newinput.shape)




    y_data['final state'] = y_data['final state'].map({'first': 1, 'second': 2, 'third': 3})
    
    smo = SMOTE(random_state=0)
    X_smo, y_smo = smo.fit_sample(X_data, y_data.values.ravel())
    X = X_smo.values
    y = y_smo.tolist()
    y = np.asarray(y)
    permutation = np.random.permutation(X.shape[0])
    
    shuffled_dataset = X[permutation, :]
    shuffled_labels = y[permutation]

    train_data = shuffled_dataset[:140, :]
    train_label = shuffled_labels[:140]

    test_data = shuffled_dataset[140:, :]
    test_label = shuffled_labels[140:]

    tree1 = buildtree(train_data, train_label, method='Gini')
    print('=============================')
    tree2 = buildtree(train_data, train_label, method='GainEnt')

    a = printtree(tree=tree1)
    b = printtree(tree=tree2)

    true_count = 0
    for i in range(len(test_label)):
        predict = classify(test_data[i], tree1)
        if predict == test_label[i]:
            true_count += 1
    print("CARTTree:{}".format(true_count))
    true_count = 0
    for i in range(len(test_label)):
        predict = classify(test_data[i], tree2)
        if predict == test_label[i]:
            true_count += 1
    print("C3Tree:{}".format(true_count))

    #print(attribute_based_on_Giniindex(X[49:51, :], y[49:51]))
    from pylab import *
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
    import treePlotter
    import matplotlib.pyplot as plt
    treePlotter.createPlot(a, 1)
    treePlotter.createPlot(b, 2)
    # 剪枝处理
    pruning(tree=tree1, alpha=4)
    pruning(tree=tree2, alpha=4)
    a = printtree(tree=tree1)
    b = printtree(tree=tree2)

    true_count = 0
    for i in range(len(test_label)):
        predict = classify(test_data[i], tree1)
        if predict == test_label[i]:
            true_count += 1
    print("CARTTree:{}".format(true_count))
    true_count = 0
    for i in range(len(test_label)):
        predict = classify(test_data[i], tree2)
        if predict == test_label[i]:
            true_count += 1
    print("C3Tree:{}".format(true_count))

    treePlotter.createPlot(a, 3)
    treePlotter.createPlot(b, 4)
    plt.show()
