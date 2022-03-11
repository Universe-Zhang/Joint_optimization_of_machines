# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 21:49
# @Author  : Zy
# @File    : calculator.py
# @Software: PyCharm

"""
本文件对给定参数计算最优解


"""

import numpy as np
#机器数量
M=3
# 时间数量
T=5
d=[50,30,60,70,60]
h = np.array([2,7,3,1,2])
p=[20,100,80,30,20]
c=[3,8,2,4,6]
cap=[[500,900,800],[520,800,900],[510,700,700],[600,650,550],[500,600,600]]
s = [100,500,330,400,350]
a=[20,25,25]
b=[50,40,60]
I = np.array([ 30,  0, 130,  60,  0])
L = np.array([0, 0, 0, 0, 0])
Q = np.array([[ 0, 0,  80,],
 [ 0,  0,  0,],
 [ 190, 0,  0,],
 [ 0,  0,  0,],
 [ 0,  0,  0,]])
y = np.array([[0, 0, 1,],
 [0, 0, 0,],
 [1,0, 0,],
 [0, 0, 0,],
 [0, 0, 0,]])
z =np.array([[0,0,0],
             [0,0,1],
             [0,1,0],
             [1,0,0],
             [0,0,0]])
tc = []

ts=[]
for i in range(T):
    tc+=[[c[i]]*M]
    ts+=[[s[i]]*M]
ta=[a]*T
tb = [b] * T
p=np.array(p).astype(int)

def calcu_x(z,y):
    x = np.zeros(z.shape)
    for t in range(z.shape[0]):
        for i in range(z.shape[1]):
            if z[t][i]==1:
                x[t][i] = 0
                continue
            if t==0:
                if y[t][i]>0:
                    x[t][i]=1
                else:
                    x[t][i] = 0
            elif y[t][i]>0:
                x[t][i]=x[t-1][i]+1
            else:
                x[t][i]=x[t-1][i]
    return x

x = calcu_x(z,y)
print(x)
# print(y)
# print(ts)
# print(y*ts)
# print(tc*Q)
# print(Q)
tc = []
ts = []
for i in range(T):
    tc += [[c[i]] * M]
    ts += [[s[i]] * M]
x = calcu_x(z, y)
# print(ta)
# print(x)
# print(tb)
# print(z)
p = np.array(p).astype(int)
# print("损失:")
# print(L)
# print("提交")
# print(submit)
# print("总支出:")
print(y)
print(ts)
print(y * ts)
print(tc)
print(Q)
print(tc * Q)
print(y * ts + tc * Q)
print(np.sum(y * ts + tc * Q))
print('----------------------')
print(h)
print(I)
print(h * I)
print(p)
print(L)
print(p * L)
print(h * I + p * L)
print(np.sum(h * I + p * L))
print('----------------------')
print(ta)
print(x)
print(ta * x)
print(tb)
print(z)
print(tb * z)
print(ta * x + tb * z)
print(np.sum(ta * x + tb * z))
total_cost = np.sum(y*ts+tc*Q)\
             +np.sum(h*I+p*L)+\
             np.sum(ta*x+tb*z)
print(total_cost)

print(np.sum(y*ts+tc*Q)\
             +np.sum(h*I+p*L))

"""
[[0 0 0]
 [0 0 0]
 [0 0 0]
 [1 1 1]
 [0 0 0]]
[[1. 0. 0.]
 [1. 0. 0.]
 [2. 0. 0.]
 [0. 0. 0.]
 [0. 0. 0.]]
1790.0
生产Q [[ 80.   0.   0.]
 [  0.   0.   0.]
 [190.   0.   0.]
 [  0.   0.   0.]
 [  0.   0.   0.]]
保持I [ 30.   0. 130.  60.   0.]
损失L [0, 0, 0, 0, 0]
"""