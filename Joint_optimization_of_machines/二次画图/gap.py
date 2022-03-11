# -*- coding: utf-8 -*-
# @Time    : 2020/6/15 13:54
# @Author  : Zy
# @File    : 收敛,时间.py
# @Software: PyCharm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

out_path = 'D:\\论文\\4机器使用的联合优化算法（未完成）\\输出\\'
img_path = 'D:\\论文\\4机器使用的联合优化算法（未完成）\\gap\\'

xi = np.arange(1,8,1)

x =[5,10,15,30,60,80,100]
x = np.array(x)
matime1 = [0,0,0.26,5.8,2.29,2.63,0.99]
matime1=np.array(matime1)

matime3 =[0,0.29,2.7,2.71,4.2]

matime3=np.array(matime3)

matime5 =[0.61,0.77,5.37,4.39,5.96]

matime5=np.array(matime5)
matime10 = [0.77,0.31,2.56,4.95,]
matime10=np.array(matime10)

matime = []
matime.append(matime1)
matime.append(matime3)
matime.append(matime5)
matime.append(matime10)
print(matime)

legend = ['M=1','M=3','M=5','M=10',]

color = ['#1f77b4','white']
edgecolor=['#1f77b4','#1f77b4']

i=0
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
marker=['.',','	,'o','v','^','<','>','1','2','3','4','s','p','*'	,'h','H','+','x','D','d','|','_']
linestyle = ['-','--','-.',':']
colors = ['b','g','r','c','m','y','k','w']
for c in matime:
    ax.plot(xi[0:c.shape[0]],
           c,
           label =legend[i],marker = marker[i],linestyle=linestyle[i])
    i=i+1
fs = 20
plt.xticks(xi,x)
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.02f'))
plt.subplots_adjust(left=0.12, right=0.99, top=0.99, bottom=0.1)
plt.tick_params(labelsize=fs)
ax.set_ylabel("Gap",fontsize = fs)
ax.set_xlabel('T',  fontsize=fs)

plt.legend(fontsize = fs)
plt.savefig(img_path+'123.png')
plt.show()





