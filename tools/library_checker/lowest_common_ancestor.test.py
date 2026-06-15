# verification-helper: PROBLEM https://judge.yosupo.jp/problem/lca

from library.graph.tree.lowest_common_ancestor import LCA


n, q = map(int, input().split())
p = list(map(int, input().split()))
t = LCA(n)

for i in range(n - 1):
    t.add_edge(i + 1, p[i])
t.build(0)

for _ in range(q):
    u, v = map(int, input().split())
    print(t.lca(u, v))
