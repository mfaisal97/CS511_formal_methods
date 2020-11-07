# Importing the z3 library
from z3 import *

###########################################

# Inputs
w = [100, 100, 100, 1, 100]
c = [[0, 7, 1, 0, 8], [7, 0, 5, 4, 3], [1, 5, 0, 2, 6], [0, 4, 2, 0, 1],
     [8, 3, 6, 1, 0]]

# Input Paramters
graph_size = len(w)

# Intermediate variables
res_to_be_optimized = 0

# Outputs
output = []
for i in range(graph_size):
    output.append(Bool('out' + str(i + 1)))

###########################################

for j in range(graph_size):
    for i in range(j):
        res_to_be_optimized += c[i][j] * Or(And(output[i], Not(output[j])),
                                            And(Not(output[i]), output[j]))

opt = Optimize()

opt.maximize(res_to_be_optimized)

print(opt.check())
print(opt.model())
