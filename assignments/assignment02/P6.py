from z3 import *

p1, p2, p3, p4 = Bools('p1 p2 p3 p4')

CNF = And (

         Or (p1, p2, p3, Not(p4)),
         Or (p1, p2, Not(p3), p4),
         Or (p1, Not(p2), p3, p4),
         Or (p1, Not(p2), Not(p3), Not(p4)),

         Or (Not(p1), p2, p3, p4),
         Or (Not(p1), p2, Not(p3), Not(p4)),
         Or (Not(p1), Not(p2), p3, Not(p4)),
         Or (Not(p1), Not(p2), Not(p3), p4)
         )

DNF = Or (
         And (Not(p1), Not(p2), Not(p3), Not(p4)),
         And (Not(p1), Not(p2), p3, p4),
         And (Not(p1), p2, Not(p3), p4),
         And (Not(p1), p2, p3, Not(p4)),

         And (p1, Not(p2), Not(p3), p4),
         And (p1, Not(p2), p3, Not(p4)),
         And (p1, p2, Not(p3), Not(p4)),
         And (p1, p2, p3, p4)         
         )

PSI = ((p1==p2) == (p3==p4))


s = Solver()
s.add(Or((CNF != DNF), (CNF != PSI), (DNF != PSI)))

print (s.check())