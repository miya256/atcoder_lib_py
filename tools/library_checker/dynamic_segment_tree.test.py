# competitive-verifier: PROBLEM https://judge.yosupo.jp/problem/point_set_range_composite_large_array

from library.range_query.segment_tree.dynamic_segment_tree import DynamicSegmentTree


def op(x, y):
    return x[0] * y[0] % mod, (y[0] * x[1] + y[1]) % mod


def e() -> tuple[int, int]:
    return 1, 0


mod = 998244353
n, q = map(int, input().split())
seg = DynamicSegmentTree(op, e(), 0, n)

for _ in range(q):
    t, *qu = map(int, input().split())
    if t == 0:
        p, c, d = qu
        seg.set(p, (c, d))
    else:
        l, r, x = qu
        a, b = seg.prod(l, r)
        print((a * x + b) % mod)
