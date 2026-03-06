def enumerate_primes(low: int, high: int) -> list[int]:
    """篩でlow以上high未満の素数を列挙"""
    is_prime = [True] * (high - low)

    if low == 0:
        primes = []
        is_prime[1] = False
        for i in range(2, high):
            if is_prime[i]:
                for j in range(i*i, high, i):
                    is_prime[j] = False
                primes.append(i)
        return primes
    
    for p in enumerate_primes(0, int(high ** 0.5) + 1):
        for i in range((low + p-1)//p * p, high, p):
            if p != i:
                is_prime[i-low] = False
    primes = [p for p in range(low, high) if is_prime[p-low]]
    return primes