def enumerate_primes(low: int, high: int) -> list[int]:
    """篩でlow以上high未満の素数を列挙"""
    is_prime = [True] * (high - low)

    if low == 0:
        p = []
        is_prime[1] = False
        for i in range(2, high):
            if is_prime[i]:
                if i*i < high:
                    for j in range(i*i, high, i):
                        is_prime[j] = False
                p.append(i)
        return p
    
    for i in enumerate_primes(0, int(high ** 0.5) + 1):
        for j in range((low+i-1)//i*i, high, i):
            if i != j:
                is_prime[j-low] = False
    p = [i for i in range(low, high) if is_prime[i-low]]
    return p