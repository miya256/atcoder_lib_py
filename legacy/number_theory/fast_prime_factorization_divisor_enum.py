#factorのappendが遅いからやっぱりspfをつかうんだ
class PrimeTable:
    def __init__(self, low, high):
        low = max(low, 1)
        self.low = low
        self.high = high
        self.sqrt_high = int(high ** 0.5)
        self._isprime = [True] * (high - low + 1) #先頭はlow
        self.primes = []
        self.factor = [[1] for _ in range(high - low + 1)]
        self._spf = [-1] * (self.sqrt_high+1)
        self._build(low, high)
    
    def _build(self, low, high):
        if low == 0:
            isprime = [True] * (high+1)
            primes = []
            for i in range(2, high+1):
                if not isprime[i]:
                    continue
                self._spf[i] = i
                for j in range(i*i, high+1, i):
                    isprime[j] = False
                    if self._spf[j] == -1:
                        self._spf[j] = i
                primes.append(i)
            return primes
        
        for i in self._build(0, self.sqrt_high):
            for j in range((low+i-1)//i*i, high+1, i):
                if self.factor[j-low][-1] * i > self.sqrt_high:
                    self.factor[j-low].append(i)
                else:
                    self.factor[j-low][-1] *= i
                if i != j:
                    self._isprime[j-low] = False
        self.primes = [i for i in range(low, high+1) if self._isprime[i-low]]
    
    def is_prime(self, n):
        assert self.low <= n <= self.high
        return self._isprime[n - self.low]
    
    def prime_factorize(self, n):
        assert self.low <= n <= self.high
        prime_factor = {}

        for factor in self.factor[n-self.low]:
            n //= factor
            while factor != 1:
                p = self._spf[factor]
                if p not in prime_factor:
                    prime_factor[p] = 0
                while factor % p == 0:
                    prime_factor[p] += 1
                    factor //= p
                while n % p == 0:
                    prime_factor[p] += 1
                    n //= p
        
        if n > 1:
            prime_factor[n] = 1
        return prime_factor
    
    def enumerate_divisors(self, n):
        assert self.low <= n <= self.high
        divisor = [1]
        for base, exp in self.prime_factorize(n).items():
            for i in range(len(divisor)):
                val = 1
                for _ in range(exp):
                    val *= base
                    divisor.append(divisor[i] * val)
        return sorted(divisor)

l,r = map(int,input().split())
pt = PrimeTable(l,r)
ans = 1
exit()
for i in range(l+1,r+1):
    if len(pt.prime_factorize(i)) == 1:
        ans += 1
print(ans)