(define-constant places (list u1 u2 u3 u4 u5))

(define-read-only (get-element (sequence (list 5 uint)) (index uint))
  (element-at? sequence index)
)

(define-read-only (get-index (elem uint))
  (index-of? places elem)
)