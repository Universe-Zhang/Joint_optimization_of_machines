# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 12:10
# @Author  : Zy
# @File    : local_search.py
# @Software: PyCharm

"""
本文件使用局部搜索算法以修理方案为DNA,LSPM联合解
为fitness
进行了实验
上个版本未添加每个机器必须维修一次的约束，本版本添加了

"""

import numpy as np

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
ta=[a]*T
tb = [b] * T

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
            if temp_full[t][i]==0<cap[t][i] and z[t][i] == 0:
                arg_s=min(cap[t][i],d[t])
                plan+=[(t,i)]
                cost+=[c[t]+s[t]/arg_s]
            # +s[i]/arg_s
        for t2 in range(0,t):
            for i in range(M):
                if temp_full[t2][i]==0 and z[t2][i]==0:
                    arg_s = min(cap[t2][i], d[t2])
                    plan += [(t2, i)]
                    if Q[t2][i]>0:
                        cost += [c[t2] + np.sum(h[t2:t]) ]
                    else:
                        cost += [c[t2] + np.sum(h[t2:t] )+s[t2]/arg_s]
                    # s[i] / arg_s+
        plan+=[(-1,-1)]
        cost+=[p[t]]
        list = np.array(cost)
        order = np.argsort(list)
        # print(order)
        sorted_cost = list[order]
        sorted_plan = np.array(plan)[order]
        # print(sorted_cost)
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
    total_cost = np.sum(y*ts+tc*Q)+np.sum(h*I+p*L)+np.sum(ta*x+tb*z)
    # print(total_cost)
    return total_cost,Q,I,L

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

N_GENERATIONS = 100
solution = np.random.randint(2, size=(T,M))
print(solution.shape)
for i in range(0,3):
    t = np.random.randint(0, T, 1)
    solution[t,i]=1
print(solution)
for i in range(N_GENERATIONS):
    m = np.random.randint(0, M,1)
    t = np.random.randint(0, T,1)
    if solution[t,m]==1 and solution[:,m].sum()==1:
        continue
    temp_s = solution.copy()
    temp_s[t,m]=1-solution[t,m]
    # if t==3:
    #     print(m,t,temp_s,produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0],solution,produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0])
    if produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0]<produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0]:
        solution=temp_s
# print(solution)
# print('----------------------------')
for i in range(N_GENERATIONS):
    m1 = np.random.randint(0, M,1)
    t1 = np.random.randint(0, T,1)
    m2 = np.random.randint(0, M, 1)
    t2 = np.random.randint(0, T, 1)
    temp_s=solution.copy()
    temp = temp_s[t2,m2]
    temp_s[t2,m2]=temp_s[t1,m1]
    temp_s[t1, m1] = temp
    if temp_s[:,m1].sum()>0 and temp_s[:,m2].sum()>0 \
            and produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0]<produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0]:
        solution=temp_s
    # print(solution)
for i in range(N_GENERATIONS):
    t1 = np.random.randint(0, T,1)
    t2 = (t1-1)%T
    temp_s = solution.copy()
    temp = temp_s[t2]
    temp_s[t2] = temp_s[t1]
    temp_s[t1] = temp
    if produce_plan(M, T, d, h, p, c, cap, s, a, b, temp_s)[0] < \
                    produce_plan(M, T, d, h, p, c, cap, s, a, b, solution)[0]:
        solution = temp_s


# for i in range(1000):
#     m1 = np.random.randint(0, M,1)
#     t1 = np.random.randint(0, T,1)
#     m2 = np.random.randint(0, M, 1)
#     t2 = np.random.randint(0, T, 1)
#     temp_s=solution.copy()
#     if temp_s[t1,m1]==1 and temp_s[t1,(m1+1)%3]==1:
#         temp_s[t1, (m1 + 1) % 3]=0
#         print('asdasd')
#     if produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0]<produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0]:
#         solution=temp_s
#     if temp_s[t2,m2]==1 and temp_s[t2,(m2-1)%3]==1:
#         temp_s[t1, (m2 + 1) % 3]=0
#         print('asdasd')
#     if produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0]<produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0]:
#         solution=temp_s
# solution=np.array([[0,0 ,0],
#  [0,0,1],
#  [0,1,0],
#  [1,0,0],
#  [0,0,0]])

print(solution)
print(produce_plan(M,T,d,h,p,c,cap,s,a,b,solution))

# (1790.0, array([[ 80.,   0.,   0.],
#        [  0.,   0.,   0.],
#        [190.,   0.,   0.],
#        [  0.,   0.,   0.],
#        [  0.,   0.,   0.]]), array([ 30.,   0., 130.,  60.,   0.]), [0, 0, 0, 0, 0])



# # [[0 0 0]
#  [0 0 0]
#  [0 0 0]
#  [1 1 0]
#  [0 0 0]] 2050.0
# [[0 0 0]
# #  [0 0 0]
# #  [0 0 0]
# #  [1 1 1]
# #  [0 0 0]] 1790.0


# [[0 0 0]
#  [0 0 0]
#  [1 0 1]
#  [0 1 0]
#  [0 0 0]]
# (1775.0, array([[ 80.,   0.,   0.],
#        [  0.,   0.,   0.],
#        [  0., 190.,   0.],
#        [  0.,   0.,   0.],
#        [  0.,   0.,   0.]]), array([ 30.,   0., 130.,  60.,   0.]), [0, 0, 0, 0, 0])