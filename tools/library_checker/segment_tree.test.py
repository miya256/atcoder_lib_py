# verification-helper: PROBLEM https://judge.yosupo.jp/problem/point_set_range_composite

from library.range_query.segment_tree.segment_tree import SegmentTree

import random


def op(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] * y[0] % mod, (y[0] * x[1] + y[1]) % mod


mod = 998244353
n, q = map(int, input().split())
ab: list[tuple] = [tuple(map(int, input().split())) for _ in range(n)]
seg = SegmentTree(op, (1, 0), ab)

for _ in range(q):
    t, *data = map(int, input().split())
    if t == 0:
        p, c, d = data
        if random.random() < 0.5:
            p -= n
        seg.set(p, (c, d))
    else:
        l, r, x = data
        if random.random() < 0.5:
            l -= n
        if r < n and random.random() < 0.5:
            r -= n
        a, b = seg.prod(l, r)
        print((a * x + b) % mod)
