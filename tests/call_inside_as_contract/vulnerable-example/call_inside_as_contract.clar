(define-public (function (contract principal) (paramA uint) (paramB uint))
    (try! (as-contract (contract-call? contract paramA paramB)))
)