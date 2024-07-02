;; Extract of a multisig-vault example

;; Cases:
;; 1) Parameter in an unique statement 
;; 2) Parameter inside a multi statements
;; 3) Parameter inside an assert! - is this a special check? (check)

(define-data-var members (list 100 principal) (list))
(define-map votes {member: principal, recipient: principal} {decision: bool})

;; offset not used
(define-private (tally (member principal) (accumulator uint) (offset int))
	(if (get-vote member tx-sender) (+ accumulator u1) accumulator)
)


(define-public (withdraw (argument_not_used uint))
	(ok 0)
)


(define-public (test-function (argument_used_inside_a_begin uint))
	(begin 
		(ok 0)
		(ok argument_used_inside_a_begin)
		(ok 1)	
	)
)

(define-read-only (test-function2 (argument_not_used_inside_a_begin uint))
	(begin 
		(ok 0)
		(ok 1)
	)	
)


(define-public (test-with-let (listing-id uint) (nft-asset-contract <nft-trait>) (payment-asset-contract <ft-trait>))
	(let (
        (notused (ok 1))
		(taker tx-sender)
		)
		(try! (assert-can-fulfil (contract-of nft-asset-contract) (some (contract-of payment-asset-contract)) listing))
		(try! (as-contract (transfer-nft nft-asset-contract (get token-id listing) tx-sender taker)))
		(try! (transfer-ft payment-asset-contract (get price listing) taker (get maker listing)))
		(map-delete listings listing-id)
		(ok listing-id)
	)
)
