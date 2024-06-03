# Var Coul Be Constant
## Description
- Vulnerability Category: `Validations and error handling`
- Severity: `Enhancement`
- Detectors: [`var-could-be-constant`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/VarCouldBeConstant.py)
- Test Cases: [`var-could-be-constant`](https://github.com/CoinFabrik/stacy/tree/main/tests/var_could_be_constant)

If you know that a variable will not change its value, you can declare it as a constant. This will optimize the contract's code.

## Exploit Scenario

```clarity

(define-data-var contract-owner tx-sender)
(define-data-var err-owner-only uint u100)
(define-data-var err-not-token-owner uint u101)
(define-data-var last-token-id uint u0)

(define-non-fungible-token stacksies uint)

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

```

The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/var_could_be_constant/vulnerable-example/var_could_be_constant.clar).

## Remediation

```clarity

(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-token-owner (err u101))

(define-non-fungible-token stacksies uint)

(define-data-var last-token-id uint u0)

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

```

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/var_could_be_constant/remediated-example/var_could_be_constant.clar).


## References
- [define-constant](https://docs.stacks.co/clarity/functions#define-constant)
