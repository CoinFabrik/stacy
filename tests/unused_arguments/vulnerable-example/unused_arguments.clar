;; Extract of a multisig-vault example

(define-constant members (list 100 principal))
(define-map votes {member: principal, recipient: principal} {decision: bool})


(define-read-only (get-vote (member principal) (recipient principal))
	(default-to false (get decision (map-get? votes {member: member, recipient: recipient})))
)

(define-private (tally (member principal) (accumulator uint) (offset int))
	(if (get-vote member tx-sender) (+ accumulator u1) accumulator)
)

(define-read-only (tally-votes (a-member principal))
	(fold tally (var-get members) u0)
)

(define-public (withdraw (argument_not_used uint))
	(ok 0)
)

(define-public (withdraw (argument_not_used uint))
	(ok 0)
)

(define-public (test-function (argument_used_inside_a_begin uint))
	(begin 
		(ok 0)
		(ok 1)
		(ok argument_used_inside_a_begin)
	)	
)

(define-read-only (test-function2 (argument_not_used_inside_a_begin uint))
	(begin 
		(ok 0)
		(ok 1)
	)	
)


(define-public (test-with-let (listing-id uint) (nft-asset-contract <nft-trait>) (payment-asset-contract <ft-trait>))
	(let 
        (not-used )
		(taker tx-sender)
		) (
		(try! (assert-can-fulfil (contract-of nft-asset-contract) (some (contract-of payment-asset-contract)) listing))
		(try! (as-contract (transfer-nft nft-asset-contract (get token-id listing) tx-sender taker)))
		(try! (transfer-ft payment-asset-contract (get price listing) taker (get maker listing)))
		(map-delete listings listing-id)
		(ok listing-id)
	)
)