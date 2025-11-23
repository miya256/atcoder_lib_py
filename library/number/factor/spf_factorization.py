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
        self._is_prime = None
        self._spf = None # iを割り切る最小の素数
        self.primes = self._enumerate_primes(n)
    
    def _enumerate_primes(self, n: int) -> list[int]:
        is_prime = [True] * (n+1)
        primes = []
        spf = [-1] * (n+1)
        is_prime[1] = False
        for i in range(2, n+1):
            if is_prime[i]:
                spf[i] = i
                for j in range(i*i, n+1, i):
                    is_prime[j] = False
                    if spf[j] == -1:
                        spf[j] = i
                primes.append(i)
        self._spf = spf
        self._is_prime = is_prime
        return primes
    
    def is_prime(self, n: int) -> bool:
        """nは素数か"""
        assert 0 < n <= self._n, f"Value error: n={n}"
        return self._is_prime[n]
    
    def prime_factorize(self, n: int) -> dict[int, int]:
        """nを素因数分解"""
        assert 0 < n <= self._n, f"Value error: n={n}"
        factor = {}
        while n > 1:
            spf = self._spf[n]
            if spf not in factor:
                factor[spf] = 0
            factor[spf] += 1
            n //= spf
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