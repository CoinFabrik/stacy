# Unused Arguments
## Description
- Vulnerability Category: `Best practices`
- Severity: `Enhancement`
- Detectors: [`unused-arguments`](https://github.com/CoinFabrik/stacy/blob/main/src/stacy_analyzer/detectors/UnusedArguments.py)
- Test Cases: [`unused-arguments`](https://github.com/CoinFabrik/stacy/tree/main/tests/unused_arguments)

If you know that a parameter passed to a function will not be used, remove it. This will optimize the contract's code and reduce gas.

## Exploit Scenario

```clarity

(define-read-only (tally-votes (member principal))
	(fold tally (var-get members) u0)
)

```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/unused_arguments/vulnerable-example/unused_arguments.clar).

## Remediation


```clarity

(define-read-only (tally-votes)
	(fold tally (var-get members) u0)
)

```

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/unused_arguments/remediated-example/unused_arguments.clar).
