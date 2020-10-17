from z3 import *

ina0, inb0, outa0, outa1, outa2, outb0 = Ints(
    'ina0 inb0 outa0 outa1 outa2 outb0')

COND_1 = ina0 == inb0
COND_2 = And(outa0 == ina0, outa1 == outa0 * ina0, outa2 == outa1 * ina0)
COND_3 = (outb0 == ((inb0 * inb0) * inb0))

Assumptions = And(COND_1, COND_2, COND_3)

IMP = Implies(Assumptions, outa2 == outb0)

s = Solver()
s.add(Not(IMP))

# prints unsat which means that the two functions output same results.
print(s.check())