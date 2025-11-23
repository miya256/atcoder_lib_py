class SegmentedSieve:
    """
    区間篩 遅いかも
    範囲が1からならspfのほう使う

    Method:
        is_prime          : 素数判定
        prime_factorize   : 素因数分解
        enumerate_divisors: 約数列挙
    """
    def __init__(self, low: int, high: int) -> None:
        assert 0 < low < high, f"Value error: [low,high)=[{low},{high})"
        self._low = low
        self._high = high
        self._is_prime = None
        self._small_primes = None
        self.primes = self._enumerate_primes(low, high)
        self._factors = self._prime_factorize(low, high)
    
    def _enumerate_primes(self, low: int, high: int) -> list[int]:
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
            self._small_primes = primes
            return primes
        
        for p in self._enumerate_primes(0, int(high ** 0.5) + 1):
            for i in range((low + p-1)//p * p, high, p):
                if p != i:
                    is_prime[i-low] = False
        self._is_prime = is_prime
        return [i for i in range(low, high) if is_prime[i-low]]
    
    def _prime_factorize(self, low: int, high: int) -> list[dict[int, int]]:
        factors = [{} for _ in range(low, high)]
        prod = [1] * (high - low)
        for p in self._small_primes:
            for i in range((low + p-1)//p * p, high, p):
                x = i
                exp = 0
                while x % p == 0:
                    x //= p
                    exp += 1
                factors[i-low][p] = exp
                prod[i-low] *= pow(p, exp)
        for i in range(low, high):
            if i // prod[i-low] != 1:
                factors[i-low][i // prod[i-low]] = 1
        return factors
    
    def is_prime(self, n: int) -> bool:
        assert self._low <= n < self._high, f"Value error: n={n}"
        return self._is_prime[n - self._low]
    
    def prime_factorize(self, n: int) -> dict[int, int]:
        assert self._low <= n < self._high, f"Value error: n={n}"
        return self._factors[n - self._low]
    
    def enumerate_divisors(self, n: int) -> list[int]:
        assert self._low <= n < self._high, f"Value error: n={n}"
        divisors = [1]
        for radix, exp in self.prime_factorize(n).items():
            for i in range(len(divisors)):
                val = 1
                for _ in range(exp):
                    val *= radix
                    divisors.append(divisors[i] * val)
        return sorted(divisors)