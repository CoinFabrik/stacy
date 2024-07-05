(define-public (function (paramA uint) (paramB uint))
	;; Keep in mind that another-contract will have the current contract as its tx-sender
	;; and the original tx-sender will be lost.
	;; Use a contract already whitelisted by you instead of letting the
	;; user pass an arbitrary contract.
	(try! (as-contract (contract-call? .fixed_contract paramA paramB)))
)