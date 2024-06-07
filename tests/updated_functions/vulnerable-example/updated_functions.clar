(define-constant places (list 1 2 3 4 5))

(define-read-only (get-element (sequence (list 5 uint)) (index uint))
  (element-at sequence index)
)

(define-read-only (get-index (elem uint))
  (index-of places elem)
)