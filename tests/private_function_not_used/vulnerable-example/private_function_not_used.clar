(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-token-owner (err u101))

(define-non-fungible-token stacksies uint)

(define-data-var last-token-id uint u0)

(define-private (get-last-token-id)
	(ok (var-get last-token-id))
)

(define-private (get-token-uri (token-id uint))
	(ok token-id)
)

(define-private (get-owner (token-id uint))
	(ok (nft-get-owner? stacksies token-id))
)

(define-public (transfer (token-id uint) (sender principal) (recipient principal))
	(begin
		(asserts! (is-eq contract-caller sender) err-not-token-owner)
		(nft-transfer? stacksies token-id sender recipient)
	)
)

(define-public (mint (recipient principal))
	(let
		(
			(token-id (+ (var-get last-token-id) u1))
		)
		(asserts! (is-eq contract-caller contract-owner) err-owner-only)
		(try! (nft-mint? stacksies token-id recipient))
		(var-set last-token-id token-id)
		(ok token-id)
	)
)
