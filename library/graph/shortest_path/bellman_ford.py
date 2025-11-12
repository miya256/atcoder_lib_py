def bellman_ford(graph: Graph, starts: list[int]) -> list[int]:
    """始点からの距離のリスト"""
    inf = 1<<61
    d = [inf] * graph.n
    for start in starts:
        d[start] = 0

    for _ in range(graph.n):
        updated = False
        for u, v, w in graph.edges:
            if d[u] != inf and d[v] > d[u] + w:
                d[v] = d[u] + w
                updated = True
        if not updated:
            break

    #負閉路の伝播
    for _ in range(graph.n):
        for u, v, w in graph.edges:
            if d[u] != inf and d[v] > d[u] + w:
                d[v] = -inf
    return d