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