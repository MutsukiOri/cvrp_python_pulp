import numpy as np
import pandas as pd
import pulp
from pulp import LpMaximize,LpInteger, LpVariable, lpDot, lpSum, value

# 各都市の距離のcsvをload
distance = np.loadtxt("./" +'distance.csv', delimiter=',', dtype='int64')
# 都市数
num = len(distance[0])

# 変数定義
# x：i→jに動けば1
x = np.array([ [ pulp.LpVariable( 'x_{}_{}'.format( i, j ), cat="Binary" ) \
        if i != j else None for j in range(len(distance[0])) ] \
        for i in range(len(distance[0])) ])
# y：都市訪問で1増える、都市"0"を訪問で0にリセット、部分巡回制約用変数
y = np.array([ [ pulp.LpVariable( 'y_{}_{}'.format( i, j ), cat=LpInteger, lowBound=0) \
        if i != j else None for j in range(len(distance[0])) ] \
        for i in range(len(distance[0])) ])

# 問題設定
problem = pulp.LpProblem( "TSP", sense=LpMaximize )

# 目的関数
problem += lpSum( distance[i][j] * x[i][j] for i in range(num) \
                        for j in range(num) if i != j )

# 制約条件
for i in range(num):
    problem += lpSum( x[i][j] for j in range(num)) == 1

for i in range(num):
    problem += lpSum( x[h][i] for h in range(num)) == 1

# flow formation 制約
for i in range(num):
    for j in range(num):
        if i == j:
            None
        else:
            problem += y[i][j] <= (x[i][j] * (num-1))

for i in range(1,len(distance[0])):
    problem += lpSum( y[i][j] for j in range(len(distance[0])) if i != j ) - lpSum( y[h][i] for h in range(len(distance[0])) if i != h ) == 1

problem += lpSum( y[0][j] for j in range(len(distance[0])) if 0 != j ) - lpSum( y[h][0] for h in range(len(distance[0])) if 0 != h ) == -(num - 1)

problem += lpSum(y[0][j] for j in range(1,num)) == 0


# 実行
result = problem.solve()

print("objective value = {}".format(pulp.value(problem.objective)))

for i in range(num):
    for j in range(num):
        if i !=j:
            if pulp.value(y[i][j]) != 0:
                print(y[i][j],pulp.value(y[i][j]))