# Private Function Not Used
## Description
- Vulnerability Category: `Validations and error handling`
- Severity: `Enhancement`
- Detectors: [`private-function-not-used`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/PrivateFunctionNotUsed.py)
- Test Cases: [`private-function-not-used`](https://github.com/CoinFabrik/stacy/tree/main/tests/private_function_not_used)

It is not a good practice to have code that is not used. This can lead to confusion and increase the size of the contract. In addition, it can also create vulnerabilities if a malicious actor finds a way to call the private functions.

## Exploit Scenario

Here we have three  private functions that are not used.

```clarity

(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-token-owner (err u101))

(define-non-fungible-token stacksies uint)

(define-data-var last-token-id uint u0)

(define-private (get-last-token-id)
	(ok (var-get last-token-id))
)

(define-private (get-token-uri (token-id uint))
	(ok none)
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



```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/private_function_not_used/vulnerable-example/private_function_not_used.clar).

## Remediation

Do not deploy smart contracts with dead code.


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

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/private_function_not_used/remediated-example/private_function_not_used.clar).

