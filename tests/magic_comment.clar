(define-data-var not-used uint u0)

(define-public (endPlay (unused-arg uint))
    (let (
        (first (get j (unwrap! (map-get? sorted {o: u0}) "err" )))
        (second (get j (unwrap! (map-get? sorted {o: u1}) "err" )))
        ;; #[allow(UnusedLetVariables, TxSenderInAssert)]
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

