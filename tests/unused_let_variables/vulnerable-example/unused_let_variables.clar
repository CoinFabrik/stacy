
(define-map play {j: principal} {hash : (buff 32)})
(define-map sorted {o: uint} {j: principal} )
(define-map to_pay  principal uint)
(define-data-var players_counter  uint u0)
(define-data-var  booleans_played int 0)
(define-data-var revelations uint u0)
(define-data-var pozo uint u0)

;; diclaimer: All the `not-used-*` arguments are catched by UnusedArguments detector

(define-public (commit_play ( hash_played (buff 32)) (amount uint))
    (if (not (is-eq u32 (len hash_played))) (begin (err "Wrong hash size"))
    (begin 
        (asserts! (not (< amount u1000000)) (err "You have to pay 1 STX"))
        (is-ok (stx-transfer? amount tx-sender (as-contract tx-sender)))
        (var-set pozo  (+ (var-get pozo ) amount))   
        (if (is-eq (var-get players_counter ) u0) (map-set sorted {o:u0} {j:tx-sender}) (map-set sorted {o:u1} {j:tx-sender}))

        (if (< (var-get players_counter ) u2)
            (begin (map-set play {j: tx-sender} {hash: hash_played}) 
                (var-set players_counter  (+ (var-get players_counter ) u1))
                (ok "Successfully added"))
            (err "There are already two players!"))))
)

(define-read-only (make_hash (bet bool) (number uint))
    (sha256 (concat (unwrap! (to-consensus-buff? bet) "err") (unwrap! (to-consensus-buff? number) "err")))
)

(define-public (show_my_play (bool_in bool) (num uint))
    (begin 
        (asserts! (not (is-none (map-get? play {j:contract-caller} ))) (err  "You are not a player" ))
        (asserts! (is-eq (make_hash bool_in num) (get hash (unwrap! (map-get? play {j:contract-caller} ) "err")))
                  (err "Do not cheat, try again") )
        (var-set revelations (+ (var-get revelations ) u1))
        (if (is-eq bool_in true) (var-set  booleans_played (+ (var-get booleans_played) 1)) 
            (var-set  booleans_played (+ (var-get booleans_played) -1)))
        (ok true)
    )
)

(define-public (getJugador (indice uint)) (get j (unwrap! (map-get? sorted {o:indice}) "err" )))


(define-public  (endPlay) 
    (let (
        (first (get j (unwrap! (map-get? sorted {o: u0}) "err" )))
        (second (get j (unwrap! (map-get? sorted {o: u1}) "err" )))
		(not-used u8)
		)

        (begin 
            (asserts!  (> (var-get revelations ) u1) (err "It can not be reveal yet!")) 
            
            (if (is-eq (var-get booleans_played) 0) 
                (begin (map-set to_pay  first  u0 ) 
                    (map-set to_pay  second (var-get pozo) ) )
                (begin (map-set to_pay  second u0) 
                    (map-set to_pay  first (var-get pozo) ) )
            )
        ) 
        (ok true)
    )
)


(define-read-only (balance) (stx-get-balance tx-sender))