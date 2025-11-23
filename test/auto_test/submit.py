def enumerate_primes(n: int) -> list[int]:
    is_prime = [True] * n
    primes = []
    is_prime[1] = False
    for i in range(2, n):
        if is_prime[i]:
            for j in range(i*i, n, i):
                is_prime[j] = False
            primes.append(i)
    return primes

def func(low: int, high: int) -> list[dict[int, int]]:
    ans = 0
    visited = [False] * (high-low)
    for p in enumerate_primes(int(high ** 0.5)+1):
        for i in range((low + p-1)//p * p, high, p):
            if visited[i-low]:
                continue
            visited[i-low] = True
            x = i
            while x % p == 0:
                x //= p
            if x == 1:
                ans += 1
    for i in range(low, high):
        if not visited[i-low]:
            ans += 1
    return ans
    

l, r = map(int,input().split())
ans = func(l+1, r+1)+1
print(ans)