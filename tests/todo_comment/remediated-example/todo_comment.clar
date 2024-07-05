(define-non-fungible-token stacksies uint)

(define-public (transfer (token-id uint) (sender principal) (recipient principal))
	(begin
		(nft-transfer? stacksies token-id sender recipient)
	)
)

(define-public (mint (recipient principal))
    ;; implementation
	(ok recipient)
)
