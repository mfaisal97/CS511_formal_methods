from z3 import *
import argparse
from random import randrange

import re

# python3 P5.py -n 4
# Check the following grid for size:      4
# ___     _R_     ___     ___
# ___     ___     ___     _Q_
# _R_     ___     ___     ___
# ___     ___     _R_     ___

# python3 P5.py -n 5
# Check the following grid for size:      5
# ___     _R_     ___     ___     ___
# ___     ___     _R_     ___     ___
# ___     ___     ___     ___     _Q_
# _R_     ___     ___     ___     ___
# ___     ___     ___     _R_     ___

# python3 P5.py -n 6
# Check the following grid for size:      6
# ___     _R_     ___     ___     ___     ___
# ___     ___     ___     ___     _Q_     ___
# _R_     ___     ___     ___     ___     ___
# ___     ___     ___     ___     ___     _Q_
# ___     ___     _R_     ___     ___     ___
# ___     ___     ___     _R_     ___     ___

# python3 P5.py -n 7
# Check the following grid for size:      7
# ___     _R_     ___     ___     ___     ___     ___
# _R_     ___     ___     ___     ___     ___     ___
# ___     ___     ___     _R_     ___     ___     ___
# ___     ___     ___     ___     ___     _R_     ___
# ___     ___     _Q_     ___     ___     ___     ___
# ___     ___     ___     ___     _R_     ___     ___
# ___     ___     ___     ___     ___     ___     _Q_

# python3 P5.py -n 8
# Check the following grid for size:      8
# ___     _R_     ___     ___     ___     ___     ___     ___
# ___     ___     _R_     ___     ___     ___     ___     ___
# ___     ___     ___     _R_     ___     ___     ___     ___
# ___     ___     ___     ___     ___     ___     _R_     ___
# ___     ___     ___     ___     ___     _R_     ___     ___
# ___     ___     ___     ___     ___     ___     ___     _Q_
# _R_     ___     ___     ___     ___     ___     ___     ___
# ___     ___     ___     ___     _Q_     ___     ___     ___


# return the places of queens and rooks
def solveQueensRooks(rows_num, cols_num, queens_rows, rooks_rows=None):
    rooks = []
    queens = []
    for i in range(rows_num):
        rooks.append([])
        queens.append([])
        for j in range(cols_num):
            rooks[i].append(Bool("Rook_" + str(i) + "_" + str(j) + "_"))
            queens[i].append(Bool("Queen_" + str(i) + "_" + str(j) + "_"))

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
                Cond_9, Implies(queens[i][j], no_other_queen_rook_in_diagonal))

    s = Optimize()
    s.add(
        And(Cond_1, Cond_2, Cond_3, Cond_4, Cond_5, Cond_6, Cond_7, Cond_8,
            Cond_9))
    s.check()
    ans = s.model()

    return ans


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
    track_cells = []
    for i in range(n):
        track_cells.append([])
        for j in range(n):
            track_cells[i].append("_")

    for var_sentence in str(res).split(","):
        var_sentence_split = var_sentence.split("_")
        i = int(var_sentence_split[1])
        j = int(var_sentence_split[2])

        if "True" in var_sentence:
            if "Queen" in var_sentence:
                track_cells[i][j] += "Q"
            if "Rook" in var_sentence:
                track_cells[i][j] += "R"
        else:
            track_cells[i][j] += "_"

    str_out = "Check the following grid for size:\t" + str(n) + "\n"
    for i in range(n):
        for j in range(n):
            str_out += (track_cells[i][j] + "\t")
        str_out += "\n"

    print(str_out)


main()
