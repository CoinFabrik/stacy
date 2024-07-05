# Unused Arguments
## Description
- Vulnerability Category: `Best practices`
- Severity: `Enhancement`
- Detectors: [`unused-arguments`]()
- Test Cases: [`unused-arguments`]()

If you know that a parameter passed to a function will not be used, remove it. This will optimize the contract's code and reduce gas.

## Exploit Scenario

```clarity

(define-read-only (tally-votes (member principal))
	(fold tally (var-get members) u0)
)

```


The vulnerable code example can be found [here]().

## Remediation


```clarity

(define-read-only (tally-votes)
	(fold tally (var-get members) u0)
)

```

The remediated code example can be found [here]().
