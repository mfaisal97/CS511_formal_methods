# The link in PDF should have directed instead to
# https://github.com/mfaisal97/CS511_formal_methods/blob/master/assignments/assignment09/CTP.py
# So I copied the related part from there to here.

from z3 import *
import argparse

import re

# grid dimensions
G = (6, 10)
# pier positions
PierP = [(1, 1), (2, 7), (3, 3), (3, 8), (6, 8)]
# blocked positions
BlockedP = [(2, 3), (2, 5), (2, 8), (4, 4), (4, 5), (4, 9), (5, 5), (6, 1)]


def AdjP(i, j, k=-1, l=-1, g=None):
    if k != -1 and l != -1 and g != None:
        return And(Or(k == i - 1, k == i + 1), k <= g[0],
                   Or(l == j - 1, l == j + 1), l <= g[1])
    elif g != None:
        return [[x, j] for x in [i - 1, i + 1] if (x <= g[0] and x > 0)
                ] + [[i, y] for y in [j - 1, j + 1] if (y <= g[1] and y > 0)]
    else:
        return []


# return: [[x1,y1],...,[xk,yk]]
def PredefinedPierPositions(G=G, PierP=PierP, BlockedP=BlockedP):
    # creating Z3py Variables
    positions = [[]]
    for i in range(1, G[0] + 1):
        positions.append([])
        positions[i].append([])
        for j in range(1, G[1] + 1):
            positions[i].append(
                Bool("Positions_" + str(i) + "_" + str(j) + "_"))

    # Constructing the optimization object
    opt = Optimize()

    # applying pier positions, C1
    for pier in PierP:
        opt.add(positions[pier[0]][pier[1]] == True)

    # applying blocked positions, C2
    for blocked in BlockedP:
        opt.add(positions[blocked[0]][blocked[1]] == False)

    # Applying C3
    for pier in PierP:
        cond = Or(False)

        # Allowing at least one neighbor per PierPosition
        for neighbor in AdjP(pier[0], pier[1], g=G):
            cond = Or(cond, positions[neighbor[0]][neighbor[1]] == True)

        # Allowing at most one neighbor per PierPosition
        for neighbor1 in AdjP(pier[0], pier[1], g=G):
            for neighbor2 in AdjP(pier[0], pier[1], g=G):
                cond = And(
                    cond,
                    Or(
                        Not(
                            And(
                                positions[neighbor1[0]][neighbor1[1]] == True,
                                Or(neighbor1[0] != neighbor2[0],
                                   Or(neighbor1[1] != neighbor2[1])))),
                        positions[neighbor2[0]][neighbor2[1]] == False))

        opt.add(cond)

    # Applying C4
    for i in range(1, G[0] + 1):
        for j in range(1, G[1] + 1):
            pos = (i, j)
            if pos not in PierP and pos not in BlockedP:
                cond = Or(False)
                for neighbor1 in AdjP(pos[0], pos[1], g=G):
                    for neighbor2 in AdjP(pos[0], pos[1], g=G):
                        cond = Or(
                            cond, Not(And(positions[pos[0]][pos[1]] == True)),
                            And(
                                positions[neighbor1[0]][neighbor1[1]] == True,
                                positions[neighbor2[0]][neighbor2[1]] == True,
                                Or(neighbor1[0] != neighbor2[0],
                                   neighbor1[1] != neighbor2[1])))
                opt.add(cond)

    # Applying the minimization for
    for i in range(1, G[0] + 1):
        for j in range(1, G[1] + 1):
            opt.add_soft(positions[i][j] == False, 0.75)

    print(opt.check())
    ans = opt.model()

    # Extracting track
    track_cells = []
    for var_sentence in str(ans).split(","):
        var_sentence_split = var_sentence.split("_")
        i = int(var_sentence_split[1])
        j = int(var_sentence_split[2])
        if "True" in var_sentence:
            track_cells.append((i, j))

    return track_cells


def main():
    # getting file_path
    input_file_path = "./input.txt"
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-f',
                           '--file',
                           action='store',
                           type=str,
                           required=False)
    args = my_parser.parse_args()

    if args.file != None:
        input_file_path = args.file

    # reading input
    with open(input_file_path, newline='') as input_file:
        file_content = input_file.read().splitlines()

        # Getting G
        g_split = re.split('\(|,|\)|=', file_content[0].split("#")[0])
        g_split = [x.strip() for x in g_split if x.strip()]
        G = (int(g_split[2]), int(g_split[3]))

        # Getting Pier
        PierP_split = file_content[1].split("#")[0].split("=")[1]
        PierP_split = re.split('\[|\]|\(|,|\)|=', PierP_split)
        PierP_split = [int(x.strip()) for x in PierP_split if x.strip()]
        pierP = []
        for i in range(int(len(PierP_split) / 2)):
            pierP.append((PierP_split[2 * i], PierP_split[2 * i + 1]))

        # print(PierP_split)
        # print(pierP)

        # Getting BlockedP
        BlockedP_split = file_content[2].split("#")[0].split("=")[1]
        BlockedP_split = re.split('\[|\]|\(|,|\)|=', BlockedP_split)
        BlockedP_split = [int(x.strip()) for x in BlockedP_split if x.strip()]
        blockedP = []
        for i in range(int(len(BlockedP_split) / 2)):
            blockedP.append((BlockedP_split[2 * i], BlockedP_split[2 * i + 1]))

        # print(BlockedP_split)
        # print(blockedP)

        res = PredefinedPierPositions(G, pierP, blockedP)
        res.sort()

        i = 0
        j = 1
        output = "[\n"
        while i < len(res) and j < G[0]:
            output += "\t"
            while i < len(res) and j < G[0]:
                if res[i][0] != j:
                    j += 1
                    break

                output += str(res[i]) + ", "
                i += 1
            output += "\n"

        output += ']'

        print(output)


main()
