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
# First Sum
first_sum = 0
for i in range(graph_size):
    first_sum += (w[i] * output[i])

# Second Sum
second_sum = 0
for j in range(graph_size):
    for i in range(j):
        second_sum += c[i][j] * And(output[i], output[j])

res_to_be_optimized = first_sum - (1 + max(w)) * second_sum

opt = Optimize()
opt.maximize(res_to_be_optimized)

print(opt.check())
print(opt.model())
