from collections import Counter

class Eratosthenes:
    def __init__(self,n):
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
                if i <= n**0.5:
                    for j in range(i*i, n+1, i):
                        isprime[j] = False
                        if self.minfactor[j] == -1:
                            self.minfactor[j] = i
                self.prime.append(i)
    
    def prime_factorize(self,n):
        if self.factor[n]:
            return self.factor[n]
        factor = []
        while n != 1:
            p = self.minfactor[n]
            while n % p == 0:
                factor.append(p)
                n //= p
        self.factor[n] = list(factor)
        return factor
    
    def enumerate_divisors(self,n):
        if self.divisor[n]:
            return self.divisor[n]
        divisor = [1]
        for base,exp in Counter(self.prime_factorize(n)).items():
            for i in range(len(divisor)):
                val = 1
                for j in range(exp):
                    val *= base
                    divisor.append(divisor[i] * val)
        self.divisor = sorted(divisor)
        return self.divisor