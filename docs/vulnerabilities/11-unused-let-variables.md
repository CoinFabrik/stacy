# Unwrap Panic Usage 
## Description
- Vulnerability Category: `Best practices`
- Severity: `Enhancement`
- Detectors: [`unused-let-variables`]()
- Test Cases: [`unused-let-variables`]()

Do not declare variables inside a `let` function if you will not used it. This will optimize the contract's code and reduce gas.

## Exploit Scenario

```clarity

(define-public  (endPlay) 
    (let (
        (first (get j (unwrap-panic (map-get? sorted {o: u0}))))
        (second (get j (unwrap-panic (map-get? sorted {o: u1}))))
		    (not-used u8)
		)
        (begin 
            (asserts!  (> (var-get revelations ) u1) (err "It can not be reveal yet!")) 
            
            (if (is-eq (var-get booleans_played) 0) 
                (begin (map-set to_pay  first  u0 ) 
                    (map-set to_pay  second (var-get pozo) ) )
                (begin (map-set to_pay  second u0) 
                    (map-set to_pay  first (var-get pozo) ) )
            )
        ) 
        (ok true)
    )
)
```


The vulnerable code example can be found [here]().

## Remediation


```clarity

(define-public  (endPlay) 
    (let (
        (first (get j (unwrap-panic (map-get? sorted {o: u0}))))
        (second (get j (unwrap-panic (map-get? sorted {o: u1}))))
		)
        (begin 
            (asserts!  (> (var-get revelations ) u1) (err "It can not be reveal yet!")) 
            
            (if (is-eq (var-get booleans_played) 0) 
                (begin (map-set to_pay  first  u0 ) 
                    (map-set to_pay  second (var-get pozo) ) )
                (begin (map-set to_pay  second u0) 
                    (map-set to_pay  first (var-get pozo) ) )
            )
        ) 
        (ok true)
    )
)

```

The remediated code example can be found [here]().



