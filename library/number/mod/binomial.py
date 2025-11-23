class Binomial:
    """
    二項係数 Mod
    """
    def __init__(self, n: int, mod: int) -> None:
        """n: n!まで計算できる"""
        fact = [1 for _ in range(n+1)]
        ifact = [1 for _ in range(n+1)]
        for i in range(1, n+1):
            fact[i] = fact[i-1] * i % mod
        ifact[n] = pow(fact[n], mod-2, mod)
        for i in range(n-1, -1, -1):
            ifact[i] = ifact[i+1] * (i+1) % mod

        self._fact = fact
        self._ifact = ifact
        self._mod = mod
        self._n = n
    
    def fact(self, n: int) -> int:
        """n!"""
        assert 0 <= n <= self._n, f"Value error: n={n}"
        return self._fact[n]
    
    def ifact(self, n: int) -> int:
        """n!^(-1)"""
        assert 0 <= n <= self._n, f"Value error: n={n}"
        return self._ifact[n]

    def permutation(self, n: int, r: int) -> int:
        """n個の中からr個選んで並べる順列の数"""
        assert n <= self._n, f"Value error: (n,r)=({n},{r})"
        if n < r or r < 0:
            return 0
        return self._fact[n] * self._ifact[n-r] % self._mod
    
    def permutation_with_repetition(self, n: int, r: int) -> int:
        """n個の中からr個 重複を許して並べる順列の個数"""
        if r < 0:
            return 0
        return pow(n, r, self._mod)

    def combination(self, n: int, r: int) -> int:
        """n個の中からr個選ぶ組み合わせの数"""
        assert n <= self._n, f"Value error: n={n}"
        if n < r or r < 0:
            return 0
        return self._fact[n] * self._ifact[r] * self._ifact[n-r] % self._mod
    
    def combination_with_repetition(self, n: int, r: int) -> int:
        """重複組み合わせ"""
        assert n+r-1 <= self._n, f"Value error: n+r-1={n+r-1}"
        return self.combination(n+r-1, r)
    
    def multiset_permutation(self, frequencies: list[int]) -> int:
        """aabbbccccのような順列"""
        assert sum(frequencies) <= self._n, f"Value error: sum(frequencies)={sum(frequencies)}"
        res = self._fact[sum(frequencies)]
        for i in frequencies:
            res = (res * self._ifact[i]) % self._mod
        return res