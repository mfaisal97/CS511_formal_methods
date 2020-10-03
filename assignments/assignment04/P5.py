from z3 import *

Being = DeclareSort('Being')

x, y, z, u = Consts('x y z u', Being)

Wolf = Function('Wolf', Being, BoolSort())
Fox = Function('Fox', Being, BoolSort())
Bird = Function('Bird', Being, BoolSort())
Caterpillar = Function('Caterpillar', Being, BoolSort())
Snail = Function('Snail', Being, BoolSort())
Animal = Function('Animal', Being, BoolSort())

Grain = Function('Grain', Being, BoolSort())
Plant = Function('Plant', Being, BoolSort())

Smaller = Function('Smaller', Being, Being, BoolSort())
Eats = Function('Eats', Being, Being, BoolSort())

COND_1_1 = And(ForAll(x, Implies(Wolf(x), Animal(x))),
               ForAll(x, Implies(Fox(x), Animal(x))),
               ForAll(x, Implies(Bird(x), Animal(x))),
               ForAll(x, Implies(Caterpillar(x), Animal(x))),
               ForAll(x, Implies(Snail(x), Animal(x))))

COND_1_2 = And(Exists(x, Wolf(x)), Exists(x, Fox(x)), Exists(x, Bird(x)),
               Exists(x, Caterpillar(x)), Exists(x, Snail(x)))

COND_2_1 = ForAll(x, Implies(Grain(x), Plant(x)))
COND_2_2 = Exists(x, Grain(x))

COND_3 = ForAll(
    x,
    Or(
        Implies(Animal(x), ForAll(y, Implies(Plant(y), Eats(x, y)))),
        ForAll(
            z,
            Implies(
                And(Animal(z), Smaller(z, x),
                    Exists(u, And(Plant(u), Eats(z, u)))), Eats(x, z)))))

COND_4 = And(
    ForAll([x, y], Implies(And(Caterpillar(x), Bird(y)), Smaller(x, y))),
    ForAll([x, y], Implies(And(Snail(x), Bird(y)), Smaller(x, y))),
    ForAll([x, y], Implies(And(Bird(x), Fox(y)), Smaller(x, y))),
    ForAll([x, y], Implies(And(Fox(x), Wolf(y)), Smaller(x, y))))

COND_5_1 = And(
    ForAll([x, y], Implies(And(Wolf(x), Fox(y)), Not(Eats(x, y)))),
    ForAll([x, y], Implies(And(Wolf(x), Grain(y)), Not(Eats(x, y)))),
    ForAll([x, y], Implies(And(Bird(x), Snail(y)), Not(Eats(x, y)))))

COND_5_2 = ForAll([x, y], Implies(And(Bird(x), Caterpillar(y)), Eats(x, y)))

COND_6 = And(
    ForAll([x, y], Implies(Caterpillar(x), Exists(y, And(Plant(y), Eats(x,
                                                                        y))))),
    ForAll([x, y], Implies(Snail(x), Exists(y, And(Plant(y), Eats(x, y))))))

TO_BE_CHECKED = Exists(
    x,
    Exists(
        y,
        And(Animal(x), Animal(y), Eats(x, y),
            ForAll(z, Implies(Grain(z), Eats(y, z))))))

axioms = And(COND_1_1, COND_1_2, COND_2_1, COND_2_2, COND_3, COND_4, COND_5_1,
             COND_5_2, COND_6)

s = Solver()

# Premises are consistent -> prints sat
s.add(axioms)
print(s.check())

# TO_BE_CHECKED is a logical result of premises -> prints unsat
s.add(Not(TO_BE_CHECKED))
print(s.check())
