def is_bipartite(graph: Graph) -> bool:
    def dfs(v: int) -> bool:
        stack = [(v, 0)]
        while stack:
            u, c = stack.pop()
            if color[u] != -1:
                if c != color[u]:
                    return False
                continue
            color[u] = c
            for v in graph[u]:
                stack.append((v, c^1))
        return True
    
    color = [-1] * graph.n
    for v in range(graph.n):
        if color[v] == -1:
            if not dfs(v):
                return False
    return True


#u-vについて、(u_a,v_b)を、(u_b,v_a)をmerge
#v_aと_v_bが同じ連結成分にあったら二部グラフでない
def is_bipartite(n: int, edges: list[tuple]) -> bool:
    uf = UnionFind(n*2)
    for u, v in edges:
        uf.merge(u, n+v)
        uf.merge(n+u, v)
    for v in range(n):
        if uf.same(v, n+v):
            return False
    return True