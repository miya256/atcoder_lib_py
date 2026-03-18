# verification-helper: PROBLEM https://judge.yosupo.jp/problem/range_affine_range_sum

from library.range_query.lazy_segment_tree.lazy_segment_tree import LazySegmentTree

import random


def op(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return (x[0] + y[0]) % mod, x[1] + y[1]


def mapping(f: tuple[int, int], x: tuple[int, int]) -> tuple[int, int]:
    return (f[0] * x[0] + f[1] * x[1]) % mod, x[1]


def composition(g: tuple[int, int], f: tuple[int, int]) -> tuple[int, int]:
    return g[0] * f[0] % mod, (g[0] * f[1] + g[1]) % mod


mod = 998244353
n, q = map(int, input().split())
a = list(map(int, input().split()))
a = [(ai, 1) for ai in a]
seg = LazySegmentTree(op, (0, 0), mapping, composition, (1, 0), a)
for _ in range(q):
    t, *data = map(int, input().split())
    if t == 0:
        l, r, b, c = data
        if random.random() < 0.5:
            l -= n
        if r < n and random.random() < 0.5:
            r -= n
        seg.apply(l, r, (b, c))
    else:
        l, r = data
        if random.random() < 0.5:
            l -= n
        if r < n and random.random() < 0.5:
            r -= n
        print(seg.prod(l, r)[0])
