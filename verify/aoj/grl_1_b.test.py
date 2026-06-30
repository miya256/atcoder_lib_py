# competitive-verifier: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/5/GRL/1/GRL_1_B

from library.graph.graph import Graph
from library.graph.shortest_path.bellman_ford import bellman_ford

inf = 1 << 61

n, m, r = map(int, input().split())
g = Graph(n)
for _ in range(m):
    s, t, d = map(int, input().split())
    g.add_edge(s, t, d)
g.build_csr()

dist = bellman_ford(g, [r])

if -inf in dist:
    print("NEGATIVE CYCLE")
    exit()

ans = [(d if d < inf else "INF") for d in dist]
print(*ans, sep="\n")
