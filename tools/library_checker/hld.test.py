# verification-helper: PROBLEM https://judge.yosupo.jp/problem/jump_on_tree

from library.graph.tree.heavy_light_decomposition import HLD

n, q = map(int, input().split())
g = HLD(n)
for _ in range(n - 1):
    a, b = map(int, input().split())
    g.add_edge(a, b)
g.build(0)
for _ in range(q):
    s, t, i = map(int, input().split())
    ans = g.jump(s, t, i)
    print(ans if ans is not None else -1)
