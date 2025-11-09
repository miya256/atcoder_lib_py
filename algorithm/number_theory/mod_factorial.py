#nCk = n-1Ck-1 + n-1Ck
class ModFactrial:
    def __init__(self,n,mod):
        """n: n!まで計算できる"""
        self.mod = mod
        fact = [1 for _ in range(n+1)]
        ifact = [1 for _ in range(n+1)]
        for i in range(1,n+1):
            fact[i] = fact[i-1] * i % mod
        ifact[-1] = pow(fact[-1],mod-2,mod)
        for i in range(n-1,-1,-1):
            ifact[i] = ifact[i+1] * (i+1) % mod
        self._fact = fact
        self._ifact = ifact
    
    def fact(self,n):
        """n!"""
        return self._fact[n]
    
    def ifact(self,n):
        """n!^-1"""
        return self._ifact[n]

    def permutation(self,n,r):
        """n個の中からr個選んで並べる順列の数"""
        return self._fact[n] * self._ifact[n-r] % self.mod
    
    def permutation_with_repetition(self,n,r):
        """重複順列"""
        return pow(n,r,self.mod)

    def combination(self,n,r):
        """n個の中からr個選ぶ組み合わせの数"""
        if n < r or r < 0:
            return 0
        return self._fact[n] * self._ifact[r] * self._ifact[n-r] % self.mod
    
    def combination_with_repetition(self,n,r):
        """重複組み合わせ"""
        return self.combination(n+r-1,r)
    
    def multiset_permutation(self,*frequencies):
        """aabbbccccのような順列"""
        res = self._fact[sum(frequencies)]
        for i in frequencies:
            res = (res * self._ifact[i]) % self.mod
        return res