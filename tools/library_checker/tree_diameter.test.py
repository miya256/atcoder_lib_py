# verification-helper: PROBLEM https://judge.yosupo.jp/problem/tree_diameter

from library.graph.tree.diameter import Diameter

n = int(input())
g = Diameter(n)
for _ in range(n - 1):
    a, b, c = map(int, input().split())
    g.add_edge(a, b, c)
    g.add_edge(b, a, c)

g.build()

r, s, t = g.diameter()

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
    for v in g[u]:
        if v == par:
            continue
        stack.append((v, u))

print(r, len(path))
print(*path)
