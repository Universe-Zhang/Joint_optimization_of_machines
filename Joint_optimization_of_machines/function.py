# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 7:54
# @Author  : Zy
# @File    : function.py
# @Software: PyCharm

import numpy as np
import math

import matplotlib.pyplot as plt
g = 0   # 改参数调节缓度
h = 1   #  坍塌速度
t = np.arange(0,20,0.1)
G = [0,1,3,5]
H = [0.1,0.5,0.8,1]
for h in H:
    y = (g+1)/(g + pow(math.e,h*t))
    plt.plot(t,y,label=h)
    plt.legend()
plt.show()

