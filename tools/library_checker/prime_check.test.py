# verification-helper: PROBLEM https://judge.yosupo.jp/problem/primality_test

from library.math.factor.prime_check import is_prime

q = int(input())
for _ in range(q):
    n = int(input())
    print("Yes" if is_prime(n) else "No")
