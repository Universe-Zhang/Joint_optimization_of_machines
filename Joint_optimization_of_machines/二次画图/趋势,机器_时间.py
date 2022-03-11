
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as mtick

x =[1,3,5,10]
x = np.array(x)
matime5 =[0.09,0.34,0.41,1.06]
macost5 = [3360,2916,3310,3418]

matime5=np.array(matime5)
macost5=np.array(macost5)

matime10 =[0.26,1.77,2.57,10.17]
macost10 = [6631,5933,5000,6552]

matime10=np.array(matime10)
macost10=np.array(macost10)

matime15 =[1,4.13,9.85,41.57]
macost15 = [6557,6835,6949,8359]

matime15=np.array(matime15)
macost15=np.array(macost15)

matime30 =[3.56,31.54,55.02,290.07]
macost30 = [15771,13855,13033,18426]

matime30=np.array(matime30)
macost30=np.array(macost30)

matime60 =[28.94,188.39,464.84,1717.51]
macost60 = [26251,31567,33352,29132]

matime60=np.array(matime60)
macost60=np.array(macost60)

matime80 =[68.81,433.35,1605.64,5335.42]
macost80 = [41511,39805,41303,44676]

matime80=np.array(matime80)
macost80=np.array(macost80)

matime100 =[128.65,1022.63,2059.06,9875.83]
macost100 = [51918,50830,46964,51735]

matime100=np.array(matime100)
macost100=np.array(macost100)


matime = []
matime.append(matime5)
matime.append(matime10)
matime.append(matime15)
matime.append(matime30)
matime.append(matime60)
matime.append(matime80)
matime.append(matime100)
print(matime)

macost = []
macost.append(macost5)
macost.append(macost10)
macost.append(macost15)
macost.append(macost30)
macost.append(macost60)
macost.append(macost80)
macost.append(macost100)
print(macost)

img_path = 'D:\\论文\\4机器使用的联合优化算法（未完成）\\5机器趋势解\\'

legend = ['MND&APP','CPLEX']
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

color = ['#1f77b4','white']
edgecolor=['#1f77b4','#1f77b4']
hatch = ['','//']
index = np.arange(0,len(x),1)
width = 0.45
i=0
f = [5,10,15,30,60,80,100]
for c in macost:
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
    ax.set_ylabel("Solution cost (10$^3$)",fontsize = fs)
    ax.set_xlabel('M',  fontsize=fs)

    img = img_path + 'M_%d_b.png' % (f[i])
    i=i+1
    # plt.show()
    plt.savefig(img)

