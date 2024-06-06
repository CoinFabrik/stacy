(define-non-fungible-token stacksies uint)

(define-public (transfer (token-id uint) (sender principal) (recipient principal))
	(begin
		;; todo: add assert
		;; false positivetodo comment test
		(nft-transfer? stacksies token-id sender recipient)
	)
)

(define-public (mint (recipient principal))
	;; TODO: implement this function
	(ok 1)
)

;; ToDo: Implement the rest of the contract