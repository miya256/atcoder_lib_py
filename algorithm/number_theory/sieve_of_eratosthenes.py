def enumerate_prime(n):
    """篩でn以下の素数を列挙"""
    isprime = [True] * (n+1)
    isprime[1] = False
    p = []
    for i in range(1, n+1):
        if isprime[i]:
            if i*i <= n:
                for j in range(i*i, n+1, i):
                    isprime[j] = False
            p.append(i)
    return p
