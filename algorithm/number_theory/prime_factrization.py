def prime_factorize(n): 
    a = []
    rn = int(n ** 0.5)
    while n % 2 == 0:
        a.append(2)
        n //= 2
    k=3
    while n != 1 and k <= rn:
        if n % k == 0:
            a.append(k)
            n //= k
        else:
            k += 2
    if n!=1:
        a.append(n)
    return a

