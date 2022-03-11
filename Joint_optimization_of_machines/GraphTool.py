# -*- coding: utf-8 -*-
# @Time    : 2020/6/20 12:18
# @Author  : Zy
# @File    : GraphTool.py
# @Software: PyCharm

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

def plot():
    legend = ['MND&APP', 'CPLEX']
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    color = ['#1f77b4', 'white']
    edgecolor = ['#1f77b4', '#1f77b4']
    hatch = ['', '//']
    index = np.arange(0, len(x), 1)
    width = 0.45
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
    ax.set_xlabel('M',  fontsize=fs)

    img = img_path + 'M_%d_b.png' % (f[i])
    i=i+1
    # plt.show()
    plt.savefig(img)

def bar(x,h,xlabel=None,ylabel=None ,save_path = None,color = None,edgecolor=None,hatch = None,fs=20,):
    if color is not None:
        color = ['#1f77b4', 'white']
    if edgecolor is not None:
        edgecolor = ['#1f77b4', '#1f77b4']
    if hatch is not None:
        hatch =  ['', '//']
    if isinstance(h, list):
        index = np.arange(0, len(h), 1)
    elif isinstance(h, np.ndarray):
        index = np.arange(0, h.shape[0], 1)
    else:
        raise Exception("数据格式错误")
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    ax.bar(index,
           h, 0.4
          , color=color[0],
           edgecolor=edgecolor[0], hatch=hatch[0])
    plt.xticks(index, x)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.02f'))
    plt.subplots_adjust(left=0.12, right=0.99, top=0.99, bottom=0.1)
    plt.tick_params(labelsize=fs)
    ax.set_ylabel(ylabel, fontsize=fs)
    ax.set_xlabel(xlabel, fontsize=fs)
    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()