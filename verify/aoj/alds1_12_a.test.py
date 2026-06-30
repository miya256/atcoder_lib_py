# competitive-verifier: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/1/ALDS1/12/ALDS1_12_A

from library.graph.graph import Graph
from library.graph.mst.kruskal import kruskal

n = int(input())
g = Graph(n)
for u in range(n):
    for v, w in enumerate(map(int, input().split())):
        if w != -1:
            g.add_edge(u, v, w)

g.build_csr()
print(kruskal(g))
