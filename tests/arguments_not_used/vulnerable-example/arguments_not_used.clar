
(define-public (transfer (token-id uint) (sender principal) (recipient principal))
	(begin
		(asserts! (is-eq contract-caller sender) err-not-token-owner)
		;;(nft-transfer? stacksies token-id sender recipient)
	)
)
