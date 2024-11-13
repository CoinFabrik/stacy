# Tx-Sender in Assert
## Description
- Vulnerability Category: `Authorization`
- Severity: `High`
- Detectors: [`tx-sender-in-assert`](https://github.com/CoinFabrik/stacy/blob/main/src/stacy_analyzer/detectors/TxSenderInAssert.py)
- Test Cases: [`tx-sender-in-assert`](https://github.com/CoinFabrik/stacy/tree/main/tests/tx_sender_in_assert)

In `Clarity`, the `tx-sender` keyword is used to get the principal of the current transaction. 

## Exploit Scenario


Since `tx-sender` can change during the execution of a contract, using it inside an `assert` statement can lead to unexpected behavior. Because of that, be mindful of the context in which `tx-sender` is used inside an assert.

```clarity

(define-public (start (new-members (list 100 principal)) (new-votes-required uint))
	(begin
		(asserts! (is-eq tx-sender contract-owner) err-owner-only)
		(asserts! (is-eq (len (var-get members)) u0) err-already-locked)
		(asserts! (>= (len new-members) new-votes-required) err-more-votes-than-members-required)
		(var-set members new-members)
		(var-set votes-required new-votes-required)
		(ok true)
	)
)

```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/tx_sender_in_assert/vulnerable-example/tx_sender.clar).

## Remediation

Only use tx-sender inside and assert only if you are sure it's not introducing a vulnerabilty 

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/tx_sender_in_assert/remediated-example/tx_sender.clar).


## References
- [tx-sender](https://docs.stacks.co/reference/keywords#tx-sender)
