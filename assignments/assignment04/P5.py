from z3 import *

# Being = DeclareSort('Being')

x, y, z, u = Ints('x y z u')

Wolf = Function('Wolf', IntSort(), BoolSort())
Fox = Function('Fox', IntSort(), BoolSort())
Bird = Function('Bird', IntSort(), BoolSort())
Caterpillar = Function('Caterpillar', IntSort(), BoolSort())
Snail = Function('Snail', IntSort(), BoolSort())
Animal = Function('Animal', IntSort(), BoolSort())

Grain = Function('Grain', IntSort(), BoolSort())
Plant = Function('Plant', IntSort(), BoolSort())

Smaller = Function('Smaller', IntSort(), IntSort(), BoolSort())
Eats = Function('Eats', IntSort(), IntSort(), BoolSort())

COND_1_1 = And(Implies(Wolf(x), Animal(x)), Implies(Fox(x), Animal(x)),
               Implies(Bird(x), Animal(x)), Implies(Caterpillar(x), Animal(x)),
               Implies(Snail(x), Animal(x)))

COND_1_2 = And(
    Exists(x, Wolf(x)),
    Exists(x, Fox(x)),
    Exists(x, Bird(x)),
    Exists(x, Caterpillar(x)),
    Exists(x, Snail(x)),
)

COND_2_1 = And(Implies(Grain(x), Plant(x)))
COND_2_2 = And(Exists(x, Grain(x)))

COND_3 = ForAll(
    x,
    Or(
        Implies(Animal(x), ForAll(y, Implies(Plant(y), Eats(x, y)))),
        ForAll(
            z,
            Implies(
                And(Animal(z), Smaller(z, x),
                    Exists(u, And(Plant(u), Eats(z, u)))), Eats(x, z)))))

COND_4 = And(Implies(And(Caterpillar(x), Bird(y)), Smaller(x, y)),
             Implies(And(Snail(x), Bird(y)), Smaller(x, y)),
             Implies(And(Bird(x), Fox(y)), Smaller(x, y)),
             Implies(And(Fox(x), Wolf(y)), Smaller(x, y)))

COND_5_1 = And(Implies(And(Wolf(x), Fox(y)), Not(Eats(x, y))),
               Implies(And(Wolf(x), Grain(y)), Not(Eats(x, y))),
               Implies(And(Bird(x), Snail(y)), Not(Eats(x, y))))

COND_5_2 = And(Implies(And(Bird(x), Caterpillar(y)), Eats(x, y)))

COND_6 = And(Implies(Caterpillar(x), Exists(y, And(Plant(y), Eats(x, y)))),
             Implies(Snail(x), Exists(y, And(Plant(y), Eats(x, y)))))

TO_BE_CHECKED = Exists(
    x,
    Exists(
        y,
        And(Animal(x), Animal(y), Eats(x, y),
            ForAll(z, Implies(Grain(z), Eats(y, z))))))

axioms = And(COND_1_1, COND_1_2, COND_2_1, COND_2_2, COND_3, COND_4, COND_5_1,
             COND_5_2, COND_6)

ALLCONDs = Not(Implies(axioms, TO_BE_CHECKED))

s = Solver()
s.add(ALLCONDs)

print(s.check())
