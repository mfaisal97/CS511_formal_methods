(declare-const p1 Bool)
(declare-const p2 Bool)
(declare-const p3 Bool)
(declare-const p4 Bool)

;Truth Table
;0   0   0   0           1
;0   0   0   1           0
;0   0   1   0           0
;0   0   1   1           1
;0   1   0   0           0
;0   1   0   1           1
;0   1   1   0           1
;0   1   1   1           0
;
;1   0   0   0           0
;1   0   0   1           1
;1   0   1   0           1
;1   0   1   1           0
;1   1   0   0           1
;1   1   0   1           0
;1   1   1   0           0
;1   1   1   1           1


(declare-fun CNF     (Bool Bool Bool Bool) Bool)
(assert
    (=
        (CNF p1 p2 p3 p4)
        (and 
            (and
                (and
                    (or (or p1 p2 ) (or p3 (not p4) ))
                    (or (or p1 p2 ) (or (not p3) p4 ))
                )
                (and
                    (or (or p1 (not p2) ) (or p3 p4 ))
                    (or (or p1 (not p2) ) (or (not p3) (not p4) ))
                )
            )
            (and
                (and
                    (or (or (not p1) p2 ) (or p3 p4 ))
                    (or (or (not p1) p2 ) (or (not p3) (not p4) ))
                )
                (and
                    (or (or (not p1) (not p2) ) (or p3 (not p4) ))
                    (or (or (not p1) (not p2) ) (or (not p3) p4 ))
                )
            )
        )
    )
)


(declare-fun DNF    (Bool Bool Bool Bool) Bool)
(assert
    (=
        (DNF p1 p2 p3 p4)
        (or 
            (or
                (or
                    (and (and (not p1) (not p2) ) (and (not p3) (not p4) ))
                    (and (and (not p1) (not p2) ) (and p3 p4 ))
                )
                (or
                    (and (and (not p1) p2 ) (and (not p3) p4 ))
                    (and (and (not p1) p2 ) (and p3 (not p4) ))
                )
            )
            (or
                (or
                    (and (and p1 (not p2) ) (and (not p3) p4 ))
                    (and (and p1 (not p2) ) (and p3 (not p4) ))
                )
                (or
                    (and (and p1 p2 ) (and (not p3) (not p4) ))
                    (and (and p1 p2 ) (and p3 p4 ))
                )
            )
        )
    )
)

    
   
(declare-fun psi (Bool Bool Bool Bool) Bool)
(assert
    (=
        (psi p1 p2 p3 p4)
        (= (= p1 p2) (= p3 p4))
    )
)
   

(assert
    (or 
        (not(= (CNF p1 p2 p3 p4) (DNF p1 p2 p3 p4)))
        (or 
            (not(= (CNF p1 p2 p3 p4) (psi p1 p2 p3 p4)))
            (not(= (DNF p1 p2 p3 p4) (psi p1 p2 p3 p4)))
        )
        
    )
)

; Since the three functions are equivalent, the check should say the assertion is not satisfiable
(check-sat)