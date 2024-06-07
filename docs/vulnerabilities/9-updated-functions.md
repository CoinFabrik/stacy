# Unwrap Panic Usage 
## Description
- Vulnerability Category: `Validations and error handling`
- Severity: `Enhancement`
- Detectors: [`updated-functions`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/UpdatedFunctionsDetector.py)
- Test Cases: [`updated-functions](https://github.com/CoinFabrik/stacy/tree/main/tests/updated_functions)

`element-at` and `index-of` are functions that changed their output signature from Clarity-1 to Clarity-2.
Since now they return an optional value, it is a good practice to make this output explicit using `element-at?` and `index-of?`.
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
