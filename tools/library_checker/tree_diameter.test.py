# verification-helper: PROBLEM https://judge.yosupo.jp/problem/tree_diameter

from library.graph.tree.tree import Tree
from library.graph.tree.diameter import diameter

n = int(input())
tree = Tree(n)
for _ in range(n - 1):
    a, b, c = map(int, input().split())
    tree.add_edge(a, b, c)

r, s, t = diameter(tree)

# s -> t のパス
path = []
stack = [(s, -1)]
while stack:
    u, par = stack.pop()
    if u < 0:
        path.pop()
        continue
    path.append(u)
    if u == t:
        break
    stack.append((~u, -1))
    for v in tree[u]:
        if v == par:
            continue
        stack.append((v, u))

print(r, len(path))
print(*path)
