# Assert Block Height 
## Description
- Vulnerability Category: `Block attributes`
- Severity: `Critical`
- Detectors: [`assert-block-height`](https://github.com/CoinFabrik/stacy/blob/main/src/stacy_analyzer/detectors/AssertBlockHeight.py)
- Test Cases: [`assert-block-height`](https://github.com/CoinFabrik/stacy/tree/main/tests/assert_block_height)

Since there is no exact method to measure time events in Stacks blockchain,`Clarity` gives you two options: `block-height` and `burn-block-height`. The main different between them is that `block-height` is based on Stacks blockchain and `burn-block-height` is based on the underlying Bitcoin blockchain.


## Exploit Scenario

One malicious user can exploit the fact block's height in Stacks is not synchronized with the Bitcoin blockchain. 


```clarity


(define-public (list-asset (nft-asset-contract <nft-trait>) (nft-asset {taker: (optional principal), token-id: uint, expiry: uint, price: uint, payment-asset-contract: (optional principal)}))
	(let ((listing-id (var-get listing-nonce)))
		(asserts! (is-whitelisted (contract-of nft-asset-contract)) err-asset-contract-not-whitelisted)
		(asserts! (> (get expiry nft-asset) block-height) err-expiry-in-past)
		(ok listing-id)
	)
)
```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/assert_block_height/vulnerable-example/assert_block_height.clar).

## Remediation

```clarity

(define-public (list-asset (nft-asset-contract <nft-trait>) (nft-asset {taker: (optional principal), token-id: uint, expiry: uint, price: uint, payment-asset-contract: (optional principal)}))
	(let ((listing-id (var-get listing-nonce)))
		(asserts! (is-whitelisted (contract-of nft-asset-contract)) err-asset-contract-not-whitelisted)
		(asserts! (> (get expiry nft-asset) burn-block-height) err-expiry-in-past)
		(ok listing-id)
	)
)
```


The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/assert_block_height/remediated-example/assert_block_height.clar).


## References
- [block-height](https://docs.stacks.co/clarity/keywords#block-height)
- [burn-block-height](https://docs.stacks.co/clarity/keywords#burn-block-height)
