# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 11:48
# @Author  : Zy
# @File    : frame.py
# @Software: PyCharm

"""
本文件使用
排序算法对生产问题LS给出了贪婪最优解
进行了实验

"""

import numpy as np
# #机器数量
# M=3
# # 时间数量
# T=5
# #每个期间的设置成本
# s=np.zeros(M)
# # 每个期间的生产成本
# c= np.zeros(T)
# # 每个期间的库存持有成本
# h = np.zeros(T)
# # 每个期间的销售成本损失
# p= np.zeros(T)
# # 每个期间的需求量
# d = np.zeros(T)
# # 每个机器的维修给用
# b = np.zeros(M)
#
# # 每个机器的生产能力
# cap = np.zeros(M,T)
#
# N = 10000
# # 机器设置的是否开机
# y = np.zeros(M,T)
# # 期间机器生产数量
# Q = np.zeros(M,T)
# # 期间的库存水平
# I = np.zeros(T)
# # 期间的销售损失
# L = np.zeros(T)
# # 自上次对机器 进行最后维修以来经过的时间
# x = np.zeros(M,T)
# # 机器的维修费用
# z = np.zeros(M,T)
# # 算法参数  缩小比率
# arg_s = 0
#机器数量
M=3
# 时间数量
T=5
d=[50,30,60,70,60]
h = [2,7,3,1,2]
p=[20,100,80,30,20]
c=[3,8,2,4,6]
cap=[[500,900,800],[520,800,900],[510,700,700],[600,650,550],[500,600,600]]
s = [100,500,330,400,350]
a=[20,25,25]
b=[50,40,60]
# z = np.zeros((T,M))
"""
[1] [3] [[0 0 0]
 [0 0 0]
 [0 0 0]
 [1 0 1]
 [0 0 0]] 2070.0 [[0 0 0]
 [0 0 0]
 [0 0 0]
 [1 1 1]
 [0 0 0]] 1790.0
"""
z = [[0,0,0],[0,0,0],[0,0,0],[1,1,1],[0,0,0]]

z = np.array(z)


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


def produce_plan(M,T,d,h,p,c,cap,s,a,b,z):
    # 机器设置的是否开机
    y = np.zeros((T,M))
    # 期间机器生产数量
    Q = np.zeros((T,M))
    # 该数组记录某点是否满,不在用其生成树
    temp_full=np.zeros((T,M))
    I = np.zeros(T)
    submit=np.zeros(T)
    for t in range(0,T):
        plan = []
        cost = []
        for i in range(M):
            # arg的初始值为该机器的生产上限和本阶段需求中的较大值
            arg_s=min(cap[t][i],d[t])
            plan+=[(t,i)]
            cost+=[c[t]+s[t]/arg_s]
            # +s[i]/arg_s
        for t2 in range(0,t):
            for i in range(M):
                if temp_full[t2][i]==0 and z[t2][i]==0:
                    arg_s = min(cap[t2][i], d[t])
                    plan += [(t2, i)]
                    cost += [c[t2] + np.sum(h[t2:t] )+s[t2]/arg_s]
                    # s[i] / arg_s+
        plan+=[(-1,-1)]
        cost+=[p[t]]
        list = np.array(cost)
        order = np.argsort(list)
        # print(order)
        sorted_cost = list[order]
        sorted_plan = np.array(plan)[order]
        #print(sorted_cost)
        # print(sorted_plan)
        # 欠缺
        shortage = d[t]
        for i in range(len(sorted_cost)):
            if sorted_cost[i]>p[t]:
                break
            # print(sorted_plan[i])
            if sorted_plan[i][0]==-1:
                continue
            if shortage>0:
                left = cap[sorted_plan[i][0]][sorted_plan[i][1]]-Q[sorted_plan[i][0]][sorted_plan[i][1]]
                if shortage>=left:
                    # print(sorted_plan[t])
                    y[sorted_plan[i][0]][sorted_plan[i][1]]=1
                    Q[sorted_plan[i][0]][sorted_plan[i][1]]+=left
                    temp_full[sorted_plan[i][0]][sorted_plan[i][1]]=1
                    if sorted_plan[i][0]!=t:
                        for temp_i in range(sorted_plan[i][0],t):
                            I[temp_i]+=left
                    submit[t]+=left
                    shortage-=left
                else:
                    y[sorted_plan[i][0]][sorted_plan[i][1]] = 1
                    Q[sorted_plan[i][0]][sorted_plan[i][1]] += shortage
                    if sorted_plan[i][0]!=t:
                        for temp_i in range(sorted_plan[i][0],t):
                            I[temp_i]+=shortage
                    submit[t] +=shortage
                    shortage=0
                    break
            else:
                break
    # print('-----------')
    # print("是否开机:")
    # print(y)
    # print("生产数量:")
    # print(Q)
    # print("库存数量:")
    # print(I)
    tc = []
    L=[]
    ts=[]
    for i in range(T):
        tc+=[[c[i]]*M]
        ts+=[[s[i]]*M]
        L+=[int(d[i]-submit[i])]
    ta=[a]*T
    tb = [b] * T
    x = calcu_x(z,y)
    # print(ta)
    # print(x)
    # print(tb)
    # print(z)
    p=np.array(p).astype(int)
    # print("损失:")
    # print(L)
    # print("提交")
    # print(submit)
    # print("总支出:")
    print(y)
    print(ts)
    print(y*ts)
    print(tc)
    print(Q)
    print(tc*Q)
    print(y*ts+tc*Q)
    print(np.sum(y*ts+tc*Q))
    print('----------------------')
    print(h)
    print(I)
    print(h*I)
    print(p)
    print(L)
    print(p*L)
    print(h*I+p*L)
    print(np.sum(h*I+p*L))
    print('----------------------')
    print(ta)
    print(x)
    print(ta*x)
    print(tb)
    print(z)
    print(tb*z)
    print(ta*x+tb*z)
    print(np.sum(ta*x+tb*z))
    total_cost = np.sum(y*ts+tc*Q)+np.sum(h*I+p*L)+np.sum(ta*x+tb*z)
    print(total_cost)
    return total_cost,Q,submit

"""
如果机器在之前开机后续对其进行排序是不要算开机

local search
算子 1   机器方向全移动（最后）



"""

print(produce_plan(M,T,d,h,p,c,cap,s,a,b,z,))