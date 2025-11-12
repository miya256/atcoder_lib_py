from heapq import heappush, heappop

def dijkstra(graph: Graph, starts: list[int]) -> list[int]:
    inf = 1 << 61
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
