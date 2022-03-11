
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as mtick


x =[5,10,15,30,60,80,100]
x = np.array(x)
matime1 = [0.09,0.26,1,3.56,28.94,68.81,128.65]
macost1 = [3360,6631,6557,15771,26251,41511,51918]
matime1=np.array(matime1)
macost1=np.array(macost1)

matime3 =[0.34,1.77,4.13,31.54,188.39,433.35,1022.63]
macost3 = [2916,5933,6835,13855,31567,39805,50830]

matime3=np.array(matime3)
macost3=np.array(macost3)

matime5 =[0.41,2.57,9.82,55.02,464.84,1605.64,2059.060]
macost5 = [3310,5000,6949,13033,33352,41303,46964]

matime5=np.array(matime5)
macost5=np.array(macost5)
matime10 = [1.06,10.17,41.57,290.07,1717.51,5335.42,9875.83]
macost10 = [3418,6552,8359,18426,29132,44676,51735]
matime10=np.array(matime10)
macost10=np.array(macost10)

cptime3 = [0.59,0.69,1.11,3.81,18.39,725.839,1549.975]
cpcost3 = [2916,5916,6655,13489,30295,38124.6628,48017.378]
cptime3=np.array(cptime3)
cpcost3=np.array(cpcost3)
cptime5 = [0.67,0.78,0.97,1.89,14.95,1210.601,1133.093]
cpcost5 = [3290,4962,6595,12485,31476,39432.4763,43578.0712]
cptime5=np.array(cptime5)
cpcost5=np.array(cpcost5)

matime = []
matime.append(matime1)
matime.append(matime3)
matime.append(matime5)
matime.append(matime10)
print(matime)

macost = []
macost.append(macost1)
macost.append(macost3)
macost.append(macost5)
macost.append(macost10)
print(macost)

img_path = 'D:\\论文\\4机器使用的联合优化算法（未完成）\\周期趋势时间\\'

legend = ['MND&APP','CPLEX']
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

color = ['#1f77b4','white']
edgecolor=['#1f77b4','#1f77b4']
hatch = ['','//']
index = np.arange(0,len(x),1)
width = 0.45
i=0
f = [1,3,5,10]
for c in matime:
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.bar(index,
           c/1000, 0.4,
           label =legend[0],color=color[0],
                       edgecolor=edgecolor[0], hatch=hatch[0])
    # ax.bar(index+0.2, cpcost5,0.4, label = legend[1],color=color[1],
    #                    edgecolor=edgecolor[1], hatch=hatch[1])
    fs = 20
    plt.xticks(index,x)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.02f'))
    plt.subplots_adjust(left=0.12, right=0.99, top=0.99, bottom=0.1)
    plt.tick_params(labelsize=fs)
    ax.set_ylabel("Running time (10$^3$)",fontsize = fs)
    ax.set_xlabel('T',  fontsize=fs)

    img = img_path + 'T_%d_b.png' % (f[i])
    i=i+1
    # plt.show()
    plt.savefig(img)