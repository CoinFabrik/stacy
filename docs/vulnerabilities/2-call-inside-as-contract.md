# Call Inside As Contract
## Description
- Vulnerability Category: `Authorization`
- Severity: `Critical`
- Detectors: [`call-inside-as-contract`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/CallInsideAsContract.py)
- Test Cases: [`call-inside-as-contract`](https://github.com/CoinFabrik/stacy/tree/main/tests/call_inside_as_contract)

In `Clarity`, when executing a contract call, the `tx-sender` is the contract that initiated the call. This means that if a contract calls another contract, the `tx-sender` of the called contract will be the calling contract. This can be exploited by a malicious contract to impersonate another contract. 

## Exploit Scenario

In this example, when Contract A calls contractB, the `tx-sender` of contractB will be Contract A and the current `tx-sender` will be lost. 

```clarity

;; Contract A

(define-public (function (contractB principal) (paramA uint) (paramB uint))
    (try! (as-contract (contract-call? contractB paramA paramB)))
)

```

The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/call_inside_as_contract/vulnerable-example/call_inside_as_contract.clar).

## Remediation

Use a contract already whitelisted by you instead of letting the user pass an arbitrary contract.

```clarity

(define-public (function (paramA uint) (paramB uint))

	(try! (as-contract (contract-call? .fixed_contract param-A param-B)))
)

```

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/call_inside_as_contract/remediated-example/call_inside_as_contract.clar).


## References
- [contract-call](https://docs.stacks.co/clarity/functions#contract-call)
- [as-contract](https://docs.stacks.co/clarity/functions#as-contract)
