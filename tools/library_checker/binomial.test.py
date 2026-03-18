# verification-helper: PROBLEM https://judge.yosupo.jp/problem/system_of_linear_equations

from library.math.mod.binomial import Binomial

t, m = map(int, input().split())
b = Binomial(min(m - 1, 10**7), m)
for _ in range(t):
    n, k = map(int, input().split())
    print(b.combination(n, k))
