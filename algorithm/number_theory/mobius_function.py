class Mobius:
    """
    2乗で割れる: 0
    因数の数が奇数個: -1
    因数の数が偶数個: +1
    """
    def __init__(self,n):
        self.n = n
        self.mobius = [1]*(n+1)
        self._eratosthenes(n)
    
    def __getitem__(self,i):
        return self.mobius[i]
    
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