# -*- coding: utf-8 -*-
# @Time    : 2019/12/19 11:48
# @Author  : Zy
# @File    : frame.py
# @Software: PyCharm
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

d=[50,30,60,70,60]
h = [2,7,3,1,2]
p=[20,35,15,30,20]
c=[30,20,25,40,20]
cap=[[100,90,80],[120,80,90],[110,70,70],[30,65,55],[50,60,60]]
s = [500,200,330]
a=[20,25,25]
b=[50,40,60]
#机器数量
M=3
# 时间数量
T=2
# 机器设置的是否开机
y = np.zeros((T,M))
# 期间机器生产数量
Q = np.zeros((T,M))
# 该数组记录某点是否满,不在用其生成树
temp_full=np.zeros((T,M))
for t in range(0,T):
    plan = []
    cost = []
    for i in range(M):
        # arg的初始值为该机器的生产上限和本阶段需求中的较大值
        arg_s=max(cap[t][i],d[t])
        plan+=[(t,i)]
        cost+=[c[i]+s[i]/arg_s]
    plan+=[(-1,-1)]
    cost+=[p[t]]
    list = np.array(cost)
    order = np.argsort(list)
    # print(order)
    sorted_cost = list[order]
    sorted_plan = np.array(plan)[order]
    print(sorted_cost)
    print(sorted_plan)
    for i in range(len(sorted_cost)):
        if sorted_cost[i]>p[t]:
            break
        print(sorted_plan[i])
        if sorted_plan[i][0]==-1:
            continue
        shortage = d[t]-sum(Q[t])
        if shortage>0:
            if shortage>cap[t][i]:
                print(sorted_plan[t])
                y[t][sorted_plan[i][1]]=1
                Q[t][sorted_plan[i][1]]+=cap[t][i]
                temp_full[t][sorted_plan[i][1]]=1
            else:
                y[t][sorted_plan[i][1]] = 1
                Q[t][sorted_plan[i][1]] += shortage
                break
print('-----------')
print(y)
print(Q)



