# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 16:32
# @Author  : Zy
# @File    : local_searchv1.2_read_file.py
# @Software: PyCharm
import xlrd
import numpy as np
import time
import copy
import pandas as pd

def load_data(file,sheet_name):
    # 打开文件
    data = xlrd.open_workbook(file)

    # 查看工作表
    data.sheet_names()
    # print("sheets：" + str(data.sheet_names()))

    # 通过文件名获得工作表,获取工作表1

    # table = data.sheet_by_name('I_%d_%d'%(m_list[0],t_list[0]))
    table = data.sheet_by_name(sheet_name)

    M = int(table.cell(1,0).value)
    T = int(table.cell(1,1).value)
    a = []
    b = []
    for i in range(1,1+M):
        a+=[int(table.cell(i,2).value)]
        b+=[int(table.cell(i,3).value)]
    # print(a,b)
    h=[]
    p=[]
    d=[]
    s=[]
    c = []
    for i in range(1,1+T):
        h+=[int(table.cell(i,4).value)]
        p+=[int(table.cell(i,5).value)]
        d+=[int(table.cell(i,6).value)]
        s+=[int(table.cell(i,7).value)]
        c+=[int(table.cell(i,8).value)]
    # print(h,p,d,s,c)
    cap = []
    for t in range(1,1+T):
        cap += [[]]
        for m in range(9,9+M):
            cap[-1]+=[int(table.cell(t,m).value)]
    # print(cap)
    return M,T,d,h,p,c,cap,s,a,b



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
            # print(temp_full.shape)
            # print(z.shape)
            # print(cap[1])
            # print(t,i)
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

N_GENERATIONS = 1000
N_STOP = 100

def local_search(M,T,d,h,p,c,cap,s,a,b):
    out_i = 0
    solution = np.random.randint(2, size=(T,M))
    calculator = 0
    n = 0
    # n_to1=0
    # n_to2=0
    # n_to3=0
    # n_eo1=0
    # n_eo2=0
    # n_eo3=0
    tc1 = time.clock()
    print(solution.shape)
    for i in range(0,M):
        t = np.random.randint(0, T, 1)
        # print(solution.shape)
        # print(t,i)
        solution[t,i]=1
    # print(solution)
    flag = True
    TABU = [{},{},{}]
    loop=0
    total = 0
    trace =pd.DataFrame(columns=('Generation','solution','running time'))
    while flag and n<N_GENERATIONS:
        for i in range(N_STOP):
            m = np.random.randint(0, M)
            t = np.random.randint(0, T)
            # print(t,m)
            # print(solution)
            # print(solution[t,m])
            # print(solution[t[0],m[0]])
            if (t, m) in TABU[0].keys():
                TABU[0][(t, m)] += 1
                loop+=1
            else:
                TABU[0][(t, m)] = 1
            total+=1
            if solution[t,m]==1 and solution[:,m].sum()==1:
                continue
            temp_s = copy.deepcopy(solution)
            temp_s[t,m]=1-solution[t,m]
            calculator +=1
            n+=1
            # n_to1+=1
            if calculator>3*N_STOP:
            # if t==3:
                flag=False
            #     print(m,t,temp_s,produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0],solution,produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0])
            if produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0]<produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0]:
                solution=temp_s
                calculator = 0
                TABU = [{}, {}, {}]
                # n_eo1+=1

            if out_i%1000==0:
                print(out_i,3*N_GENERATIONS)
            out_i+=1
        # print(solution)
        # print('----------------------------')
        for i in range(N_STOP):
            m1 = np.random.randint(0, M)
            t1 = np.random.randint(0, T)
            m2 = np.random.randint(0, M)
            t2 = np.random.randint(0, T)
            if (t1, m1, t2, m2) in TABU[1].keys():
                TABU[0][(t1, m1, t2, m2)]+=1
                loop+=1
            else:
                TABU[0][(t1, m1, t2, m2)] = 1
            total+=1
            temp_s=copy.deepcopy(solution)
            temp = copy.deepcopy(temp_s[t2,m2])
            temp_s[t2,m2]=copy.deepcopy(temp_s[t1,m1])
            temp_s[t1, m1] = copy.deepcopy(temp)
            calculator +=1
            n+=1
            # n_to2+=1
            if calculator>3*N_STOP:
                flag=False
            if temp_s[:,m1].sum()>0 and temp_s[:,m2].sum()>0 \
                    and produce_plan(M,T,d,h,p,c,cap,s,a,b,temp_s)[0]<produce_plan(M,T,d,h,p,c,cap,s,a,b,solution)[0]:
                solution=temp_s
                calculator = 0
                TABU = [{}, {}, {}]
                # n_eo2+=1

            if out_i%1000==0:
                print(out_i,3*N_GENERATIONS)
            out_i += 1
        for i in range(N_STOP):
            t1 = np.random.randint(0, T)
            if (t1) in TABU[2].keys():
                TABU[0][(t1)]+=1
                loop+=1
            else:
                TABU[0][(t1)] = 1
            total+=1
            t2 = (t1-1)%T
            temp_s = copy.deepcopy(solution)
            temp = copy.deepcopy(temp_s[t2])
            temp_s[t2] = copy.deepcopy(temp_s[t1])
            temp_s[t1] = copy.deepcopy(temp)
            calculator +=1
            n+=1
            # n_to3+=1
            if calculator>3*N_STOP:
                flag=False
            v1  = produce_plan(M, T, d, h, p, c, cap, s, a, b, temp_s)[0]
            v2 = produce_plan(M, T, d, h, p, c, cap, s, a, b, solution)[0]
            m = v2
            if v1 < v2:
                solution = temp_s
                m = v1
                calculator = 0
                TABU = [{}, {}, {}]
                # n_eo3+=1
            if out_i%1000==0:
                print(out_i,3*N_GENERATIONS)
            out_i += 1
        tc2 = time.clock()
        trace =   trace.append({'Generation':n,'solution':m,'running time':tc2-tc1}, ignore_index=True,)
    # print(n_eo1,n_to1)
    # print(n_eo2,n_to2)
    # print(n_eo3,n_to3)
    trace.to_csv(out_path+'Inst_%d_%d.csv'%(M,T))
    print(loop,total)
    return solution

path = 'data\\Instances_LS\\'
# files_name=['Instance_1_Machine.xlsx','Instance_3_Machines.xlsx','Instance_5_Machines.xlsx','Instance_10_Machines.xlsx']
m_list = [10]
t_list = [100]
# files_name=['Instance_5_Machines. xlsx']
out_path = 'data\\output\\'
# t_list = [30]
# m_list = [10]

for sti, st in enumerate(t_list):
    for fi,fn in enumerate(m_list):
        file = path+'Inst_%d_%d.xlsx'%(m_list[fi],t_list[sti])
        sheet_name = 'I_%d_%d'%(m_list[fi],t_list[sti])
        # print(file)
        # print(sheet_name)
        M, T, d, h, p, c, cap, s, a, b = load_data(file,sheet_name)
        N_GENERATIONS=m_list[fi]*t_list[sti]*10
        # N_STOP = m_list[fi]*t_list[sti]
        N_STOP = 50
        # time_1 = time.clock()

        solution = local_search(M,T,d,h,p,c,cap,s,a,b)
        # time_2 = time.clock()
        # print(sheet_name,solution,produce_plan(M, T, d, h, p, c, cap, s, a, b, solution))
        print(sheet_name,produce_plan(M, T, d, h, p, c, cap, s, a, b, solution)[0])
        # print('running time:',time_2-time_1)
"""
I_5_30
9235.0

十几次二十几次

472.0622401

452.60565410000004

"""