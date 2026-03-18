# verification-helper: PROBLEM https://judge.yosupo.jp/problem/staticrmq

from library.range_query.sparse_table import SparseTable

import random

n, q = map(int, input().split())
a = list(map(int, input().split()))
st = SparseTable(min, a)

for _ in range(q):
    l, r = map(int, input().split())
    if random.random() < 0.5:
        l -= n
    if r < n and random.random() < 0.5:
        r -= n
    print(st.prod(l, r)[0])
