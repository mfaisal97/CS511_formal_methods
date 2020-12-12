from z3 import *
import argparse
from random import randrange

import re

# The code checks if this condition holds for each condition:
# Whether there is exist a model where 8 conditions are satified
# and at the same time the ninth condition is violated
# when the check returns unsat, the condition is marked as not necessary
# Below I used 15 (base case for infinite model)
# (Cond[0 : i-1, i+1 : n]) ^ (-Cond[i])

# python3 P5.py -n 15
# Condition 1 is not necessary:   False
# Condition 2 is not necessary:   False
# Condition 3 is not necessary:   False
# Condition 4 is not necessary:   True
# Condition 5 is not necessary:   False
# Condition 6 is not necessary:   True
# Condition 7 is not necessary:   False
# Condition 8 is not necessary:   False
# Condition 9 is not necessary:   False


# returns conditions of a specific problem
def getConditions(rows_num, cols_num, queens_rows, rooks_rows=None, ind=0):
    rooks = []
    queens = []
    for i in range(rows_num):
        rooks.append([])
        queens.append([])
        for j in range(cols_num):
            rooks[i].append(
                Bool(str(ind) + "_Rook_" + str(i) + "_" + str(j) + "_"))
            queens[i].append(
                Bool(str(ind) + "_Queen_" + str(i) + "_" + str(j) + "_"))

    # 1.  There is a queen on each of the selected rows:
    Cond_1 = True
    for i in queens_rows:
        row_cond = False
        for j in range(cols_num):
            row_cond = Or(row_cond, queens[i][j])
        Cond_1 = And(Cond_1, row_cond)

    # 2.  There is a rook on each of the remaining(n−p) rows:
    if rooks_rows == None:
        rooks_rows = [x for x in range(rows_num) if x not in queens_rows]
    Cond_2 = True
    for i in rooks_rows:
        row_cond = False
        for j in range(cols_num):
            row_cond = Or(row_cond, rooks[i][j])
        Cond_2 = And(Cond_2, row_cond)

    # 3.  No position on the board contains both aqueenand aknight:
    Cond_3 = True
    for i in range(rows_num):
        for j in range(cols_num):
            Cond_3 = And(Cond_3, Implies(queens[i][j], Not(rooks[i][j])))

    # 4. On every row i, if there is a queen in column j,
    # then there is norookand no otherqueenon row i:
    Cond_4 = True
    for i in range(rows_num):
        for j in range(cols_num):
            no_other_queen_rook_in_row = True
            for l in range(cols_num):
                if l != j:
                    no_other_queen_rook_in_row = And(
                        no_other_queen_rook_in_row, Not(rooks[i][l]),
                        Not(queens[i][l]))
            Cond_4 = And(Cond_4,
                         Implies(queens[i][j], no_other_queen_rook_in_row))

    # 5.  On every column j, if there is a queen in row i,
    # then there is no rook and no other queenon column j:
    Cond_5 = True
    for i in range(rows_num):
        for j in range(cols_num):
            no_other_queen_rook_in_col = True
            for k in range(rows_num):
                if k != i:
                    no_other_queen_rook_in_col = And(
                        no_other_queen_rook_in_col, Not(rooks[k][j]),
                        Not(queens[k][j]))
            Cond_5 = And(Cond_5,
                         Implies(queens[i][j], no_other_queen_rook_in_col))

    # 6.  On every row i, if there is arookin column j,
    # then there is noqueenand no otherrookon row i:
    Cond_6 = True
    for i in range(rows_num):
        for j in range(cols_num):
            no_other_queen_rook_in_row = True
            for l in range(cols_num):
                if l != j:
                    no_other_queen_rook_in_row = And(
                        no_other_queen_rook_in_row, Not(rooks[i][l]),
                        Not(queens[i][l]))
            Cond_6 = And(Cond_6,
                         Implies(rooks[i][j], no_other_queen_rook_in_row))

    # 7. On every column j, if there is a rook in row i,
    # then there is no queen and no other rook on column j:
    Cond_7 = True
    for i in range(rows_num):
        for j in range(cols_num):
            no_other_queen_rook_in_col = True
            for k in range(rows_num):
                if k != i:
                    no_other_queen_rook_in_col = And(
                        no_other_queen_rook_in_col, Not(rooks[k][j]),
                        Not(queens[k][j]))
            Cond_7 = And(Cond_7,
                         Implies(rooks[i][j], no_other_queen_rook_in_col))

    # 8. On every diagonal, if there is a queen,
    # there is no rook and no otherqueenon the same diagonal:
    Cond_8 = True
    for i in range(rows_num):
        for j in range(cols_num):
            no_other_queen_rook_in_diagonal = True
            for k in range(rows_num):
                for l in range(cols_num):
                    if k - l == i - j and k != i and l != j:
                        no_other_queen_rook_in_diagonal = And(
                            no_other_queen_rook_in_diagonal, Not(rooks[k][l]),
                            Not(queens[k][l]))
            Cond_8 = And(
                Cond_8, Implies(queens[i][j], no_other_queen_rook_in_diagonal))

    # 9. On every antidiagonal, if there is a queen,
    # there is no rook and no other queen on the same antidiagonal:
    Cond_9 = True
    for i in range(rows_num):
        for j in range(cols_num):
            no_other_queen_rook_in_anti_diagonal = True
            for k in range(rows_num):
                for l in range(cols_num):
                    if k + l == i + j and k != i and l != j:
                        no_other_queen_rook_in_anti_diagonal = And(
                            no_other_queen_rook_in_anti_diagonal,
                            Not(rooks[k][l]), Not(queens[k][l]))
            Cond_9 = And(
                Cond_9,
                Implies(queens[i][j], no_other_queen_rook_in_anti_diagonal))

    return [
        Cond_1, Cond_2, Cond_3, Cond_4, Cond_5, Cond_6, Cond_7, Cond_8, Cond_9
    ]


# return the places of queens and rooks
def solveQueensRooks(rows_num, cols_num, queens_rows, rooks_rows=None):

    unncessary_condition = []
    for i in range(9):
        s = Optimize()
        conds = getConditions(rows_num, cols_num, queens_rows, rooks_rows, i)
        # unncessary_condition.append(Bool("Unnecessary_COND_" + str(i) + "_"))
        implies_premise = True
        for j in range(9):
            if j != i:
                implies_premise = And(implies_premise, conds[j])

        s.add(And(implies_premise, Not(conds[i])))

        unncessary_condition.append(str(s.check()))

    return unncessary_condition


# Generate random subset from :
# https://www.codementor.io/@alexanderswilliams/how-to-efficiently-generate-a-random-subset-150hbz3na4


def shuffle(list):
    n = len(list)
    for i in range(n - 1):
        j = randrange(i, n - 1)  # i <= j < n
        value = list[i]
        list[i] = list[j]
        list[j] = value


def getDistinctRandomNumbers(inclusiveMin, exclusiveMax, amount):
    result = set()
    while len(result) != amount:
        result.add(randrange(inclusiveMin, exclusiveMax))
    return result


def getRandomElements(list, amount):
    length = len(list)
    amount = min(length, amount)
    if amount < 0.63212055882 * length:
        randomNumbers = getDistinctRandomNumbers(0, length, amount)
        result = [None] * amount
        i = 0
        for num in randomNumbers:
            result[i] = list[num]
            i += 1
        return result
    else:
        shuffle(list)
        return list[0:amount]


def generate_random_subset(max_elements, elements_number):
    return getRandomElements(list(range(max_elements)), elements_number)


def main():
    set_option(max_args=10000000,
               max_lines=1000000,
               max_depth=10000000,
               max_visited=1000000)

    n = 3
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-n',
                           '--number',
                           action='store',
                           type=int,
                           required=False)
    args = my_parser.parse_args()

    if args.number != None:
        n = args.number

    queens_rows = generate_random_subset(n, int(n / 3))
    res = solveQueensRooks(n, n, queens_rows)

    # Extracting grid
    track_conds = []
    for i in range(9):
        track_conds.append("Condition " + str(i + 1) + " is not necessary: \t")
        if res[i] == "sat":
            track_conds[i] += "False"
        else:
            track_conds[i] += "True"

    # for var_sentence in str(res).split(","):
    #     if "Unnecessary_COND_" in var_sentence:
    #         var_sentence_split = var_sentence.split("_")
    #         i = int(var_sentence_split[2])

    #         if "True" in var_sentence:
    #             track_conds[i] += "True"
    #         else:
    #             track_conds[i] += "False"

    for cond in track_conds:
        print(cond)


main()
