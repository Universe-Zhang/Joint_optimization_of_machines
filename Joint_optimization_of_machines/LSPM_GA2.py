# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 12:01
# @Author  : Zy
# @File    : repair_GA.py
# @Software: PyCharm

"""
本文件使用进化算法以修理方案为DNA,LSPM联合解为fitness
进行了实验

相比于1,本文件将准备在交叉策略(主要)和选择策略上做出一定改进,增大其收敛性

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
            if temp_full[t][i] == 0 and z[t][i] == 0:
                arg_s=min(cap[t][i],d[t])
                plan+=[(t,i)]
                cost+=[c[t]+s[t]/arg_s]
            # +s[i]/arg_s
        for t2 in range(0,t):
            for i in range(M):
                if temp_full[t2][i]==0 and z[t2][i]==0:
                    arg_s = min(cap[t2][i], d[t2])
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
    total_cost = np.sum(y*ts+tc*Q)+np.sum(h*I+p*L)+np.sum(ta*x+tb*z)
    # print(total_cost)
    return total_cost,Q,I,L

DNA_SIZE = T*M        # 40 x moves, 40 y moves
CROSS_RATE = 0.8
MUTATE_RATE = 0.1
POP_SIZE = 100
N_GENERATIONS = 100


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

class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size,a,b ):
        self.DNA_size = DNA_size
        # DNA_bound[1] += 1
        # self.DNA_bound = DNA_bound
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.a = a
        self.b = b
        self.pop = np.random.randint(2, size=(pop_size, DNA_size))

    def DNA2product(self, DNA,):                 # convert to readable string
        pop = DNA.reshape((POP_SIZE,DNA_SIZE))
        return pop

    def get_fitness(self, pop,a,b):
        fitness =np.zeros(POP_SIZE)
        for i,z in enumerate(pop):
            z=z.reshape((T,M))
            # x = calcu_x(z,y)
            fitness[i],_,_,_=produce_plan(M,T,d,h,p,c,cap,s,a,b,z,)
        return fitness

    def select(self, fitness):
        ones=np.ones(fitness.shape)
        fitness_2 = ones/fitness
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, )
        #p=fitness_2/fitness_2.sum()
        return self.pop[idx]
    """
    这个交叉策略为,首先对父代按fitness排序,按照顺序挨个选取一个父亲,如果随机数超过交叉率,则随机算取种群中另一个,
    并且随机选50%的位置,将后者拓印个前者,这里类似于微生物进化算法
    """
    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)  # select another individual from pop
            # print("parent1:",parent)
           #  print("parent2:", pop[i_])
            cross_points = np.random.randint(0, 1, self.DNA_size).astype(np.bool)   # choose crossover points
          #   print("cp:",cross_points)
            f1 = self.get_fitness(parent.reshape((1,DNA_SIZE)),a,b)
            f2 = self.get_fitness(pop[i_].reshape((1, DNA_SIZE)), a, b)
            # if f1.sum()>f2.sum():
            parent[cross_points] = pop[i_, cross_points]       # mating and produce one child
           #  print('after:',parent)


        return parent

    def crossover2(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)  # select another individual from pop
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)   # choose crossover points
            parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
        return parent


    def mutate(self, child):
        for i in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[i] = 1-child[i]
        return child

    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop



ga = GA(DNA_size=DNA_SIZE,
        cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE,a=a,b=b)

minv = 10000
minplan=[]
for generation in range(N_GENERATIONS):
    pop = ga.DNA2product(ga.pop,)
    fitness = ga.get_fitness(pop,a,b)
    ga.evolve(fitness)
    print(fitness.min())
    print(pop[fitness.argmin()].reshape((T,M)))
    if fitness.min()<minv:
        minv=fitness.min()
        minplan = pop[fitness.argmin()].reshape((T,M))
    print('Gen:', generation, '| best fit:', fitness.min())

print(minv)
print(minplan)
fitness,Q,I,L=produce_plan(M,T,d,h,p,c,cap,s,a,b,minplan,)
print(calcu_x(minplan,Q) )
print(fitness)
print("生产Q",Q)
print("保持I",I)
print("损失L",L)


