# The link in PDF should have directed instead to
# https://github.com/mfaisal97/CS511_formal_methods/blob/master/assignments/assignment09/CTP.py
# So I copied the related part from there to here.

from z3 import *

# input >> modeling the example in the slides

# list ofConditional Probability Tables(CPTs)
# CPTs: [(V,T)]
# T: [(Cs,(V,v),p)]
# Cs: [(X,x)]
# Not(), represents a' ... And represents a
# Notice that I used only the pointer
T1 = [([], ("x1", And), 0.3), ([], ("x1", Not), 0.7)]
CPT1 = ("x1", T1)

T2 = [([], ("x2", And), 0.2), ([], ("x2", Not), 0.8)]
CPT2 = ("x2", T2)

T3 = [([], ("x3", And), 0.9), ([], ("x3", Not), 0.1)]
CPT3 = ("x3", T3)

T4 = [([("x1", And), ("x2", And)], ("x4", And), 0.2),
      ([("x1", And), ("x2", And)], ("x4", Not), 0.8),
      ([("x1", And), ("x2", Not)], ("x4", And), 0.9),
      ([("x1", And), ("x2", Not)], ("x4", Not), 0.1),
      ([("x1", Not), ("x2", And)], ("x4", And), 0.1),
      ([("x1", Not), ("x2", And)], ("x4", Not), 0.9),
      ([("x1", Not), ("x2", Not)], ("x4", And), 0.6),
      ([("x1", Not), ("x2", Not)], ("x4", Not), 0.4)]
CPT4 = ("x4", T4)

T5 = [([("x2", And), ("x3", And)], ("x5", And), 0.5),
      ([("x2", And), ("x3", And)], ("x5", Not), 0.5),
      ([("x2", And), ("x3", Not)], ("x5", And), 0.6),
      ([("x2", And), ("x3", Not)], ("x5", Not), 0.4),
      ([("x2", Not), ("x3", And)], ("x5", And), 0.3),
      ([("x2", Not), ("x3", And)], ("x5", Not), 0.7),
      ([("x2", Not), ("x3", Not)], ("x5", And), 0.1),
      ([("x2", Not), ("x3", Not)], ("x5", Not), 0.9)]
CPT5 = ("x5", T5)

T6 = [([("x5", And)], ("x6", And), 0.1), ([("x5", And)], ("x6", Not), 0.9),
      ([("x5", Not)], ("x6", And), 0.5), ([("x5", Not)], ("x6", Not), 0.5)]
CPT6 = ("x6", T6)

T7 = [([("x4", And)], ("x7", And), 0.7), ([("x4", And)], ("x7", Not), 0.3),
      ([("x4", Not)], ("x7", And), 0.4), ([("x4", Not)], ("x7", Not), 0.6)]
CPT7 = ("x7", T7)

T8 = [([("x4", And), ("x5", And)], ("x8", And), 0.4),
      ([("x4", And), ("x5", And)], ("x8", Not), 0.6),
      ([("x4", And), ("x5", Not)], ("x8", And), 0.5),
      ([("x4", And), ("x5", Not)], ("x8", Not), 0.5),
      ([("x4", Not), ("x5", And)], ("x8", And), 0.6),
      ([("x4", Not), ("x5", And)], ("x8", Not), 0.4),
      ([("x4", Not), ("x5", Not)], ("x8", And), 0.7),
      ([("x4", Not), ("x5", Not)], ("x8", Not), 0.3)]
CPT8 = ("x8", T8)

CPTS = [CPT1, CPT2, CPT3, CPT4, CPT5, CPT6, CPT7, CPT8]

# list ofobservations(Os)
# Os: [(randomVar, itsValue)]
Os = [("x5", Not), ("x6", Not), ("x7", Not), ("x8", Not)]

# list of random variables (Vs)
# Vs: [randomVar]
Vs = ["x1", "x2", "x3", "x4"]


# Problem 06
# Maximum Aposteriori Probability(MAP)
# return: [["V1",v1],...,["Vn",vn]]
def MAP(CPTs, Os, Vs):
    # creating Z3py Variables
    Xs = dict()
    for cpt in CPTs:
        Xs[cpt[0]] = Bool(cpt[0])

    # applying observations, enforced using the add function
    opt = Optimize()
    for v in Os:
        opt.add(v[1](Xs[v[0]]))

    # To ignore optimizating the variables not mentioned in the Vs
    needed_variables = Vs + [x[0] for x in Os]

    # applying weighted caluse, using the soft_add
    for cpt in CPTs:
        if cpt[0] in needed_variables:
            for row in cpt[1]:
                cond = Not(row[1][1](Xs[row[1][0]]))
                for cs in row[0]:
                    cond = Or(cond, Not(cs[1](Xs[cs[0]])))

                opt.add_soft(cond, -math.log(row[2], 10))

    print(opt.check())
    return opt.model()


print(MAP(CPTS, Os, Vs))