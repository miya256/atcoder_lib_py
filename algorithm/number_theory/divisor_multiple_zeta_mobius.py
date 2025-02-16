class ZetaMobiusTransform:
    def __init__(self,n):
        self.n = n
        self.mobius = [1]*(n+1)
        self.prime = []
        self._eratosthenes(n)
    
    def _eratosthenes(self,n):
        isprime = [True] * (n+1)
        isprime[1] = False
        for i in range(2, n+1):
            if isprime[i]:
                self.mobius[i] = -1
                for j in range(i*2, n+1, i):
                    isprime[j] = False
                    if j // i % i == 0:
                        self.mobius[j] = 0
                    else:
                        self.mobius[j] = -self.mobius[j]
                self.prime.append(i)
    
    def divisor_zeta_transform(self,f):
        """累積maxとかもできる
        f(i) -> F(i)
        f[i] = iの約数dについてf[d]の総和　になる
        つまりiの個数 -> iの約数の個数(6なら、1,2,3,6の個数の和)
        """
        for p in self.prime:
            for i in range(1,self.n//p+1):
                f[i*p] += f[i]
        return f
    
    def divisor_mobius_transform(self,f):
        for p in self.prime:
            for i in range(self.n//p,0,-1):
                f[i*p] -= f[i]
        return f
    
    def multiplier_zeta_transform(self,f):
        """
        f(i) -> F(i)
        f[i] = iの倍数のfの総和　になる
        つまりiの個数 -> iの倍数の個数(iを約数に持つものの個数)になる
        """
        for p in self.prime:
            for i in range(self.n//p,0,-1):
                f[i] += f[i*p]
        return f
    
    def multiplier_mobius_transform(self,f,x=None):
        """
        F(i) -> f(i)
        xが与えられなければ全部求めて配列を返す
        xが与えられたらf(x)を返す
        """
        if x:
            res = 0
            for i in range(1,self.n//x+1):
                res += self.mobius[i] * f[i*x]
            return res
        for p in self.prime:
            for i in range(1,self.n//p+1):
                f[i] -= f[i*p]
        return f