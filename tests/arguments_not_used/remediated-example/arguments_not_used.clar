;; multisig-vault
;; A simple multisig vault that allows members to vote on who should receive the STX contents.

(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-already-locked (err u101))
(define-constant err-more-votes-than-members-required (err u102))
(define-constant err-not-a-member (err u103))
(define-constant err-votes-required-not-met (err u104))

(define-constant members (list 100 principal) (list))
(define-constant votes-required uint u1)
(define-map votes {member: principal, recipient: principal} {decision: bool})


(define-read-only (get-vote (member principal) (recipient principal))
	(default-to false (get decision (map-get? votes {member: member, recipient: recipient})))
)

(define-private (tally (member principal) (accumulator uint))
	(if (get-vote member tx-sender) (+ accumulator u1) accumulator)
)

(define-read-only (tally-votes)
	(fold tally (var-get members) u0)
)

(define-public (withdraw)
	(let
		(
			(recipient tx-sender)
			(total-votes (tally-votes))
		)
		(asserts! (>= total-votes (var-get votes-required)) err-votes-required-not-met)
		(try! (as-contract (stx-transfer? (stx-get-balance tx-sender) tx-sender recipient)))
		(ok total-votes)
	)
)
