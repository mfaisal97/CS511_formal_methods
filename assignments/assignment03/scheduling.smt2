(set-logic QF_LIA)
(set-option :produce-models true)

;adding tasks limits
(declare-fun A () Int)
(assert (>= A 0))
(declare-fun At () Int)
(assert (= At 2))

(declare-fun B () Int)
(assert (>= B 0))
(declare-fun Bt () Int)
(assert (= Bt 1))

(declare-fun C () Int)
(assert (>= C 0))
(declare-fun Ct () Int)
(assert (= Ct 2))

(declare-fun D () Int)
(assert (>= D 0))
(declare-fun Dt () Int)
(assert (= Dt 2))
(declare-fun E () Int)

(assert (>= E 0))
(declare-fun Et () Int)
(assert (= Et 7))

(declare-fun F () Int)
(assert (>= F 0))
(declare-fun Ft () Int)
(assert (= Ft 5))

;Tasks A and C may not overlap.
(assert (or (<= (+ A At) C) (<= (+ C Ct) A)))

;No two of tasks B, D or E can overlap.
(assert (or (<= (+ B Bt) D) (<= (+ D Dt) B)))
(assert (or (<= (+ B Bt) E) (<= (+ E Et) B)))
(assert (or (<= (+ D Dt) E) (<= (+ E Et) D)))

;Tasks D and E must be completed before task F starts.
(assert (and (<= (+ D Dt) F) (<= (+ E Et) F)))

;Task A must complete before B starts.
(assert (<= (+ A At) B))

;just putting an end
(declare-fun End () Int)
(assert (= End 14))

(assert (<= (+ A At) End))
(assert (<= (+ B Bt) End))
(assert (<= (+ C Ct) End))
(assert (<= (+ D Dt) End))
(assert (<= (+ E Et) End))
(assert (<= (+ F Ft) End))

(check-sat)
; (get-model) ; un-comment if you want to see details of the model
(get-value (A B C D E F))
