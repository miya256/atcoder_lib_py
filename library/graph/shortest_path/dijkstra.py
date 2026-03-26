from library.graph.graph import Graph
from heapq import heappush, heappop

inf = 1 << 61


def dijkstra(graph: Graph, starts: list[int]) -> list[int]:
    dist = [inf] * graph.n
    hq = []
    for s in starts:
        dist[s] = 0
        hq.append((0, s))

    while hq:
        d, u = heappop(hq)
        if d > dist[u]:
            continue
        for v, w in graph(u):
            if d + w < dist[v]:
                dist[v] = d + w
                heappush(hq, (d + w, v))
    return dist
