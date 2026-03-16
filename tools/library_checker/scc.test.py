# verification-helper: PROBLEM https://judge.yosupo.jp/problem/scc

from library.graph.directed.scc_kosaraju import SCC

n, m = map(int, input().split())
g = SCC(n, m)
for _ in range(m):
    a, b = map(int, input().split())
    g.add_edge(a, b)

g.build()

scc = g.scc()

print(len(scc))
for component in scc:
    print(len(component), *component)
