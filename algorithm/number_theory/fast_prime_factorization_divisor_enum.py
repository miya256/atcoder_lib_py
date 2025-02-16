class Eratosthenes:
    def __init__(self,n):
        """n以下"""
        self.n = n
        self.minfactor = [-1]*(n+1) #iを割り切れる最小の素数
        self.prime = []
        self.factor = [None]*(n+1)
        self.divisor = [None]*(n+1)

        self.eratosthenes(n)
    
    def eratosthenes(self,n):
        isprime = [True] * (n+1)
        isprime[1] = False
        self.minfactor[1] = 1
        for i in range(1, n+1):
            if isprime[i]:
                self.minfactor[i] = i
                if i*i <= n:
                    for j in range(i*i, n+1, i):
                        isprime[j] = False
                        if self.minfactor[j] == -1:
                            self.minfactor[j] = i
                self.prime.append(i)
    
    def prime_factorize(self,n):
        if self.factor[n]:
            return self.factor[n]
        factor = {}
        x = n
        while x != 1:
            p = self.minfactor[x]
            factor[p] = 1
            x //= p
            while x % p == 0:
                factor[p] += 1
                x //= p
        self.factor[n] = dict(factor)
        return factor
    
    def enumerate_divisors(self,n):
        if self.divisor[n]:
            return self.divisor[n]
        divisor = [1]
        for base,exp in self.prime_factorize(n).items():
            for i in range(len(divisor)):
                val = 1
                for _ in range(exp):
                    val *= base
                    divisor.append(divisor[i] * val)
        self.divisor[n] = sorted(divisor)
        return self.divisor[n]