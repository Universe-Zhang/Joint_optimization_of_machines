# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 16:23
# @Author  : Zy
# @File    : draft.py
# @Software: PyCharm
# import numpy as np
#
# z = [[1,0,0],[0,1,0],[0,0,0],[0,0,0],[0,0,1]]
#
# z = np.array(z)
#
# def calcu_x(z):
#     x = np.zeros(z.shape)
#     for t in range(z.shape[0]):
#         for i in range(z.shape[1]):
#             if z[t][i]==1:
#                 x[t][i] = 0
#                 continue
#             if t==0:
#                 x[t][i]=1
#             else:
#                 x[t][i]=x[t-1][i]+1
#     return x
# a=[20,25,25]
# b=[50,40,60]
# x = calcu_x(z)
# print(x)
# print(np.sum(a*x+b*z))
import numpy as np
d=[50,30,60,70,60]
h = [2,7,3,1,2]
p=[2,10,8,3,2]
c=[3,8,2,4,6]
cap=[[500,900,800],[520,800,900],[510,700,700],[600,650,550],[500,600,600]]
print(min((cap[1][1], d[1])))
cap = np.array(cap)
print(cap[:,2])