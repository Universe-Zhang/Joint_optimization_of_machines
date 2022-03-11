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
img_path = 'D:\\论文\\4机器使用的联合优化算法（未完成）\\收敛趋势代数\\'

m_list = [3,5,10]
t_list = [15,30,60,80,100]
for fi,fn in enumerate(m_list):
    for sti,st in enumerate(t_list):
        file = out_path+'Inst_%d_%d.csv'%(m_list[fi],t_list[sti])
        df = pd.read_csv(file)
        print(df.head())
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(111)
        x = df['Generation'].tolist()
        y = df['solution'].to_list()
        y = np.array(y)
        fs = 20
        plt.tick_params(labelsize=fs)
        plt.xlabel('Generation', fontsize=fs)
        plt.ylabel('Solution cost (10$^3$)', fontsize=fs)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.02f'))
        plt.plot(x, y/1000 )

        plt.subplots_adjust(left=0.12, right=0.99,top=0.99,bottom=0.1)
        img = img_path+'Inst_%d_%d_b.png'%(m_list[fi],t_list[sti])
        plt.savefig(img)
        # plt.show()


