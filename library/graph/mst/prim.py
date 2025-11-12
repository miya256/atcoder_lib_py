from heapq import heappush, heappop

def prim(graph: Graph) -> int:
    """最小全域木"""
    visited = [False] * graph.n
    node_count = 0
    weight = 0
    hq = [(0, 0)]
    while node_count < graph.n:
        w, u = heappop(hq)
        if visited[u]:
            continue
        visited[u] = True
        weight += w
        node_count += 1
        for v, w in graph(u):
            if visited[v]:
                continue
            heappush(hq, (w ,v))
    return weight