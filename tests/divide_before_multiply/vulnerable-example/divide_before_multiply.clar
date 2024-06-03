;; In clarity, the decimals are dropped. So if you divide before multiply, you end up losing precision

(define-public (sharing-a-prize (participants uint) (prize uint) (bonus uint)) 
    (* (/ prize participants) bonus)
)