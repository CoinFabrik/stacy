# TODO comment
## Description
- Vulnerability Category: `Best practices`
- Severity: `Enhancement`
- Detectors: [`todo-comment`](https://github.com/CoinFabrik/stacy/blob/main/stacks_analyzer/detectors/ToDoComment.py)
- Test Cases: [`todo-comment`](https://github.com/CoinFabrik/stacy/tree/main/tests/todo_comment)

As a best practice, it is recommended to remove `TODO` comments from the code. 

## Exploit Scenario

```Clarity

(define-public (mint (recipient principal))
	;; TODO: implement this function
	(ok 1)
)

;; ToDo: Implement the rest of the contract

```

The vulnerable code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/todo_comment/vulnerable-example/todo_comment.clar).

## Remediation

Remove unnecessary comments from the code before deploying it. 

```Clarity

(define-public (mint (recipient principal))
	;; corresponding implementation
)

```

The remediated code example can be found [here](https://github.com/CoinFabrik/stacy/blob/main/tests/todo_comment/remediated-example/todo_comment.clar).


