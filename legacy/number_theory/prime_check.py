def isprime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

#ミラーラビン法
#※まちがってる
#a^(p-1) - 1 = 0なので、a^(p-1) - 1の因数のどれかは0になる
def isprime(n):
    s,t = 0,n-1
    while t % 2 == 0:
        s += 1
        t >>= 1
    for a in [(2,7,61), (2,325,9375,28178,450775,9780504,1795265022)][n >= 475912314]:
        x = pow(a,t,n)
        if x != 1: #a^t == 1なら素数の可能性あり
            i = 0
            while i < s:
                if x == n-1: #a^(t*2^i) == -1なら素数の可能性あり
                    break
                x = x * x % n
                i += 1
            if i == s:
                return False
    return True