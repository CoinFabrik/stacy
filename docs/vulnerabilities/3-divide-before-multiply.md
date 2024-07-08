# Divide Before Multiply
## Description
- Vulnerability Category: `Arithmetic`
- Severity: `Medium`
- Detectors: [`divide-before-multiply`](https://github.com/CoinFabrik/stacy/blob/main/src/stacy_analyzer/detectors/DivideBeforeMultiply.py)
- Test Cases: [`divide-before-multiply`](https://github.com/CoinFabrik/stacy/tree/main/tests/divide_before_multiply)

In `Clarity`, decimals are dropped after an arithmetic operation. This can lead to an undesired loss of precision if the order of operations is not correct. 

## Exploit Scenario

```clarity

(define-public (sharing-a-prize (participants uint) (prize uint) (bonus uint)) 
    (* (/ prize participants) bonus)
)
```


The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/divide_before_multiply/vulnerable-example/divide_before_multiply.clar).

## Remediation

By changing the order, we can avoid losing precision in intermidiate steps.

```clarity

(define-public (sharing-a-prize (participants uint) (prize uint) (bonus uint)) 
    (/ (* prize bonus) participants)
)
```


The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/divide_before_multiply/remediated-example/divide_before_multiply.clar).



## References
- [Primitive-types](https://book.clarity-lang.org/ch02-01-primitive-types.html)
