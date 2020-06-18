
import numpy as np

def cross_f(zu1,zu2):
    result=[]
    for i in range(len(zu1)):
        #zhuanzhi=zu1[i].T
        jieguo=zu1[i][:,None]*zu2[i]
        jieguo=jieguo.reshape(1,-1)
        result.append(jieguo)
    resnp=np.array(result).squeeze()
    return resnp
zu1=np.array([[0,0,1,0],
     [1,0,0,0],
     [1,0,0,0],
     [0,0,0,1]])
zu2=np.array([[0,0,1,0,0],
     [1,0,0,0,0],
     [1,0,0,0,0],
     [0,0,0,1,0]])
a=cross_f(zu1,zu2)
print(a)