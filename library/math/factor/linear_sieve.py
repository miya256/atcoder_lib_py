def enumerate_primes(low: int, high: int) -> list[int]:
    """
    篩でlow以上high未満の素数を列挙
    定数倍のせいか、エラトステネスの篩のほうが速かった
    """
    # 線形篩
    if low == 0:
        primes = []
        lpf = [None] * high
        for i in range(2, high):
            if lpf[i] is None:
                lpf[i] = i
                primes.append(i)
            for p in primes:
                if p * i >= high or p > lpf[i]:
                    break
                lpf[p * i] = p
        return primes
    
    is_prime = [True] * (high - low)
    for p in enumerate_primes(0, int(high ** 0.5) + 1):
        for i in range((low + p-1)//p * p, high, p):
            if p != i:
                is_prime[i-low] = False
    primes = [p for p in range(low, high) if is_prime[p-low]]
    return primes