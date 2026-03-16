# verification-helper: PROBLEM https://judge.yosupo.jp/problem/unionfind

from library.connectivity.union_find import UnionFind

n, q = map(int, input().split())
uf = UnionFind(n)
for _ in range(q):
    t, u, v = map(int, input().split())
    if t == 0:
        uf.merge(u, v)
    else:
        print(1 if uf.same(u, v) else 0)
