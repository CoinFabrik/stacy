# Unwrap Panic Usage 
## Description
- Vulnerability Category: `Validations and error handling`
- Severity: `Minor`
- Detectors: [`unwrap-panic-usage`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/UnwrapPanicUsage.py)
- Test Cases: [`unwrap-panic-usage`](https://github.com/CoinFabrik/stacy/tree/main/tests/unwrap_panic_usage)

The `unwrap-panic` function attempts to 'unpack' its argument. If it fails, it throws a runtime error, which aborts the execution of the current transaction.

## Exploit Scenario

```clarity


(define-public (fulfil-listing-ft (listing-id uint) (nft-asset-contract <nft-trait>) (payment-asset-contract <ft-trait>))
	(let 
        (listing (unwrap-panic (map-get? listings listing-id) err-unknown-listing))
		(taker tx-sender)
		) (
		(try! (assert-can-fulfil (contract-of nft-asset-contract) (some (contract-of payment-asset-contract)) listing))
		(try! (as-contract (transfer-nft nft-asset-contract (get token-id listing) tx-sender taker)))
		(try! (transfer-ft payment-asset-contract (get price listing) taker (get maker listing)))
		(map-delete listings listing-id)
		(ok listing-id)
	)
)

```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/unwrap_panic_usage/vulnerable-example/unwrap_panic.clar).

## Remediation

Use `unwrap!` instead of `unwrap-panic` to handle the error.

```clarity

(define-public (fulfil-listing-ft (listing-id uint) (nft-asset-contract <nft-trait>) (payment-asset-contract <ft-trait>))
	(let 
        (listing (unwrap! (map-get? listings listing-id) err-unknown-listing))
		(taker tx-sender)
		) (
		(try! (assert-can-fulfil (contract-of nft-asset-contract) (some (contract-of payment-asset-contract)) listing))
		(try! (as-contract (transfer-nft nft-asset-contract (get token-id listing) tx-sender taker)))
		(try! (transfer-ft payment-asset-contract (get price listing) taker (get maker listing)))
		(map-delete listings listing-id)
		(ok listing-id)
	)
)
```

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/unwrap_panic_usage/remediated-example/unwrap_panic.clar).



## References
- [unwrap-panic](https://docs.stacks.co/clarity/functions#unwrap-panic)
