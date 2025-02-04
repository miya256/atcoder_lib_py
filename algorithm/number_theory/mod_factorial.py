class ModFactrial:
    def __init__(self,mod,n):
        """n: (n-1)!まで計算できる"""
        self.mod = mod
        _fact = [1 for _ in range(n)]
        _ifact = [1 for _ in range(n)]
        for i in range(1,n):
            _fact[i] = _fact[i-1] * i % mod
        _ifact[-1] = pow(_fact[-1],mod-2,mod)
        for i in range(n-2,-1,-1):
            _ifact[i] = _ifact[i+1] * (i+1) % mod
        self._fact = _fact
        self._ifact = _ifact
    
    def fact(self,n):
        """n!"""
        return self._fact[n]
    
    def ifact(self,n):
        """n!^-1"""
        return self._ifact[n]

    def perm(self,n,k):
        """n個の中からk個選んで並べる順列の数"""
        return self._fact[n] * self._ifact[n-k] % self.mod
    
    def multi_perm(self,n,r):
        """重複順列"""
        return pow(n,r,self.mod)

    def comb(self,n,k):
        """n個の中からk個選ぶ組み合わせの数"""
        if n < k or k < 0:
            return 0
        return self._fact[n] * self._ifact[k] * self._ifact[n-k] % self.mod
    
    def multi_comb(self,n,r):
        """重複組み合わせ"""
        return self.comb(n+r-1,r)
    
    def multi_perm(self,*k):
        """aabbbccccのような順列"""
        res = self._fact[sum(k)]
        for i in k:
            res = (res * self._ifact[i]) % self.mod
        return res
