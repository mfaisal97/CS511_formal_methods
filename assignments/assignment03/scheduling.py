from z3 import *

A, At, B, Bt, C, Ct, D, Dt, E, Et, F, Ft, End = Ints('A At B Bt C Ct D Dt E Et F Ft End')


#adding tasks limits
CONDTASKS = And (

         A >= 0,
         B >= 0,
         C >= 0,
         D >= 0,
         E >= 0,
         F >= 0,

         At == 2,
         Bt == 1,
         Ct == 2,
         Dt == 2,
         Et == 7,
         Ft == 5
         )

#Tasks A and C may not overlap.
COND1 = Or (
    (A + At) <= C,
    (C + Ct) <= A
    )


#No two of tasks B, D or E can overlap.
COND2 = And(
    Or (
        (B + Bt) <= D,
        (D + Dt) <= B
    ), Or (
        (B + Bt) <= E,
        (E + Et) <= B
    ), Or (
        (D + Dt) <= E,
        (E + Et) <= D
    )
)


#Tasks D and E must be completed before task F starts.
COND3 = And (
    (D + Dt) <= F,
    (E + Et) <= F
)


#Task A must complete before B starts.
COND4 = ((A + At) <= B)


#Putting a termination for the process.
CONDEND = And (
    End == 14,
    (A + At) <= End,
    (B + Bt) <= End,
    (C + Ct) <= End,
    (D + Dt) <= End,
    (E + Et) <= End,
    (F + Ft) <= End

)

# adding the output of the z3 code given in the pdf as a condition for testing
# if not passed then the formulation is not correct (one way)
# CONDTEST = And (
#     End == 14,
#     A == 0,
#     B == 9,
#     C == 2,
#     D == 0,
#     E == 2,
#     F == 9
# )
# solve(And (CONDTASKS, COND1, COND2, COND3, COND4, CONDEND, CONDTEST))


solve(And (CONDTASKS, COND1, COND2, COND3, COND4, CONDEND))
