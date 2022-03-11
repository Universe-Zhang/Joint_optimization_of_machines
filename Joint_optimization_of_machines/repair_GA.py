# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 12:01
# @Author  : Zy
# @File    : repair_GA.py
# @Software: PyCharm

"""
本文件使用进化算法以修理方案为DNA,维修问题PM为fitness
进行了实验

"""

import numpy as np

#机器数量
M=3
# 时间数量
T=5
z = np.zeros((T,M))
a=[20,25,25]
b=[50,40,60]
ta=[a]*T
tb = [b] * T

DNA_SIZE = T*M        # 40 x moves, 40 y moves
CROSS_RATE = 0.8
MUTATE_RATE = 0.0001
POP_SIZE = 100
N_GENERATIONS = 500


def calcu_x(z):
    x = np.zeros(z.shape)
    for t in range(z.shape[0]):
        for i in range(z.shape[1]):
            if z[t][i]==1:
                x[t][i] = 0
                continue
            if t==0:
                x[t][i]=1
            else:
                x[t][i]=x[t-1][i]+1
    return x

class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size, ):
        self.DNA_size = DNA_size
        # DNA_bound[1] += 1
        # self.DNA_bound = DNA_bound
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size

        self.pop = np.random.randint(2, size=(pop_size, DNA_size))

    def DNA2product(self, DNA,):                 # convert to readable string
        pop = DNA.reshape((POP_SIZE,DNA_SIZE))
        return pop

    def get_fitness(self, pop,a,b):
        fitness =np.zeros(POP_SIZE)
        for i,z in enumerate(pop):
            z=z.reshape((T,M))
            x = calcu_x(z)
            fitness[i]=np.sum(ta*x+tb*z)
        return fitness

    def select(self, fitness):
        ones=np.ones(fitness.shape)
        fitness_2 = ones/fitness
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness_2/fitness_2.sum())
        return self.pop[idx]

    def crossover(self, parent, pop):
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
        cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE)

min = 10000
minplan=[]
for generation in range(N_GENERATIONS):
    pop = ga.DNA2product(ga.pop,)
    fitness = ga.get_fitness(pop,a,b)
    ga.evolve(fitness)
    if fitness.min()<min:
        min=fitness.min()
        minplan = pop[fitness.argmin()].reshape((T,M))
    print('Gen:', generation, '| best fit:', fitness.min())
print(min)
print(minplan)

