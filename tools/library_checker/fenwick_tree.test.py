# verification-helper: PROBLEM https://judge.yosupo.jp/problem/point_add_range_sum

from library.range_query.fenwick_tree.fenwick_tree import FenwickTree

import random

n, q = map(int, input().split())
a = list(map(int, input().split()))
ft = FenwickTree(a)

for _ in range(q):
    t, *data = map(int, input().split())
    if t == 0:
        p, x = data
        # 負のindexも試す
        if random.random() < 0.5:
            p -= n
        ft.add(p, x)
    else:
        l, r = data
        if random.random() < 0.5:
            l -= n
        if r < n and random.random() < 0.5:
            r -= n
        print(ft.sum(l, r))
