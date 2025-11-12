def kruskal(graph: Graph) -> int:
    """最小全域木の重み"""
    edges = graph.edges
    edges.sort(key=lambda x:x[-1])
    uf = UnionFind(graph.n)
    weight = 0
    for u, v, w in edges:
        if uf.same(u, v):
            continue
        weight += w
        uf.merge(u, v)
    return weight