class PrimeTable:
    """
    素因数分解などを O(nloglogn) で計算
    n以下の数字の多くを素因数分解したいときとか

    Method:
        is_prime          : 素数判定
        prime_factorize   : 素因数分解
        enumerate_divisors: 約数列挙
    """

    def __init__(self, n: int) -> None:
        self._n = n
        self._lpf = None # iを割り切る最小の素数
        self.primes = self._enumerate_primes(n)
    
    def _enumerate_primes(self, n: int) -> list[int]:
        primes = []
        lpf = [-1] * (n+1)
        for i in range(2, n+1):
            if lpf[i] == -1:
                lpf[i] = i
                for j in range(i*i, n+1, i):
                    if lpf[j] == -1:
                        lpf[j] = i
                primes.append(i)
        self._lpf = lpf
        return primes
    
    def is_prime(self, n: int) -> bool:
        """nは素数か"""
        assert 0 < n <= self._n, f"Value error: n={n}"
        return self._lpf[n] == n
    
    def prime_factorize(self, n: int) -> dict[int, int]:
        """nを素因数分解"""
        assert 0 < n <= self._n, f"Value error: n={n}"
        factor = {}
        while n > 1:
            lpf = self._lpf[n]
            if lpf not in factor:
                factor[lpf] = 0
            factor[lpf] += 1
            n //= lpf
        return factor
    
    def enumerate_divisors(self, n: int) -> list[int]:
        """nの約数を列挙"""
        assert 0 < n <= self._n, f"Value error: n={n}"
        divisors = [1]
        for radix, exp in self.prime_factorize(n).items():
            for i in range(len(divisors)):
                val = 1
                for _ in range(exp):
                    val *= radix
                    divisors.append(divisors[i] * val)
        return sorted(divisors)