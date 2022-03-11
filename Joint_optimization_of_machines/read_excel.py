# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 15:40
# @Author  : Zy
# @File    : read_excel.py
# @Software: PyCharm

import xlrd

path = 'D:\\论文\\机器使用的联合优化算法\\'
files_name=['Instance_1_Machine.xlsx','Instance_3_Machine.xlsx','Instance_5_Machine.xlsx','Instance_10_Machine.xlsx']
m_list = [1,3,5,10]
t_list = [5,10,15,30,60,80,100]

# 打开文件
data = xlrd.open_workbook(path+files_name[0])

# 查看工作表
data.sheet_names()
print("sheets：" + str(data.sheet_names()))

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('I_%d_%d'%(m_list[0],t_list[0]))

M = int(table.cell(1,0).value)
T = int(table.cell(1,1).value)
a = []
b = []
for i in range(1,1+M):
    a+=[int(table.cell(i,2).value)]
    b+=[int(table.cell(i,3).value)]
print(a,b)
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
print(h,p,d,s,c)
cap = []
for m in range(9,9+M):
    cap+=[[]]
    for t in range(1,1+T):
        cap[-1]+=[int(table.cell(t,m).value)]
print(cap)

# 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
# table = data.sheet_by_index(0)

# 获取行数和列数
# 行数：table.nrows
# 列数：table.ncols
# print("总行数：" + str(table.nrows))
# print("总列数：" + str(table.ncols))
#
# # 获取整行的值 和整列的值，返回的结果为数组
# # 整行值：table.row_values(start,end)
# # 整列值：table.col_values(start,end)
# # 参数 start 为从第几个开始打印，
# # end为打印到那个位置结束，默认为none
# print("整行值：" + str(table.row_values(0)))
# print("整列值：" + str(table.col_values(1)))
#
# # 获取某个单元格的值，例如获取B3单元格值
# cel_B3 = table.cell(3,2).value
# print("第三行第二列的值：" + cel_B3)