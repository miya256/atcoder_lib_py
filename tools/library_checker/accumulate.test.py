# verification-helper: PROBLEM https://judge.yosupo.jp/problem/static_range_sum

from library.range_query.accumulate import Accumulation

n, q = map(int, input().split())
a = list(map(int, input().split()))
acc = Accumulation(a)

for _ in range(q):
    l, r = map(int, input().split())
    print(acc.sum((l,), (r,)))
