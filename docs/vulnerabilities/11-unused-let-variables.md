# Unwrap Panic Usage 
## Description
- Vulnerability Category: `Best practices`
- Severity: `Enhancement`
- Detectors: [`unused-let-variables`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/UpdatedFunctionsDetector.py)
- Test Cases: [`unused-let-variables`](https://github.com/CoinFabrik/stacy/tree/main/tests/updated_functions)


## Exploit Scenario

```clarity

(define-constant places (list 1 2 3 4 5))

(define-read-only (get-element (sequence (list 5 uint)) (index uint))
  (element-at sequence index)
)

(define-read-only (get-index (elem uint))
  (index-of places elem)
)

```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/updated_functions/vulnerable-example/undated_functions.clar).

## Remediation

Use the latest version of Clarity and update the functions to the new signature.

```clarity

(define-constant places (list 1 2 3 4 5))

(define-read-only (get-element (sequence (list 5 uint)) (index uint))
  (element-at? sequence index)
)

(define-read-only (get-index (elem uint))
  (index-of? places elem)
)
```

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/updated_functions/remediated-example/undated_functions.clar).



## References
- [index-of](https://docs.stacks.co/clarity/functions#index-of)
- [index-of?](https://docs.stacks.co/clarity/functions#index-of?)
- [element-at](https://docs.stacks.co/clarity/functions#element-at)
- [element-at?](https://docs.stacks.co/clarity/functions#element-at?)
