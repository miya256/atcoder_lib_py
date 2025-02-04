def eratosthenes(n):
    isprime = [True] * (n+1)
    isprime[1] = False
    p = []
    for i in range(1, n+1):
        if isprime[i]:
            if i <= n**0.5:
                for j in range(i*i, n+1, i):
                    isprime[j] = False
            p.append(i)
    return p
