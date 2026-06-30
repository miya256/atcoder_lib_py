# competitive-verifier: PROBLEM https://judge.yosupo.jp/problem/vertex_add_subtree_sum

from library.range_query.fenwick_tree.fenwick_tree import FenwickTree
from library.graph.tree.tree import Tree
from library.graph.tree.euler_tour import euler_tour


n, q = map(int, input().split())
a = list(map(int, input().split()))
p = list(map(int, input().split()))
tree = Tree(n)
for i in range(n - 1):
    tree.add_edge(i + 1, p[i])

_, in_time, out_time, _, node_weight, *_ = euler_tour(tree, 0)
ft = FenwickTree(node_weight)
for i in range(n):
    ft.set(in_time[i], a[i])

for _ in range(q):
    t, *data = map(int, input().split())
    if t == 0:
        u, x = data
        ft.add(in_time[u], x)
    else:
        u = data[0]
        print(ft.sum(in_time[u], out_time[u]))
