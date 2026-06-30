# competitive-verifier: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/5/GRL/1/GRL_1_C

from library.graph.shortest_path.warshall_floyd import WarshallFloyd

inf = 1 << 61

n, m = map(int, input().split())
g = WarshallFloyd(n)
for _ in range(m):
    s, t, d = map(int, input().split())
    g.add_edge(s, t, d)
g.build()

if g.has_negative_cycle:
    print("NEGATIVE CYCLE")
    exit()


for u in range(n):
    ans = [(g.dist(u, v) if g.dist(u, v) < inf else "INF") for v in range(n)]
    print(*ans)
