# 通る点のmaxが少ないようにBFSしたとき、maxがk以下か

from heapq import heappush, heappop

def dijkstra(graph, starts: list[int]) -> list[int]:
    inf = 1 << 61
    dist = [inf] * n
    hq = []
    for s in starts:
        dist[s] = 0
        hq.append((0, s))

    while hq:
        d, u = heappop(hq)
        if d > dist[u]:
            continue
        for v in graph[u]:
            if max(d, v) < dist[v]:
                dist[v] = max(d,v)
                heappush(hq, (max(d,v), v))
    return dist

n,m = map(int,input().split())
g = [[] for _ in range(n)]
for _ in range(m):
    u,v = map(lambda x: int(x)-1,input().split())
    g[u].append(v)

dist = dijkstra(g, [0])
for i in range(n-1):
    dist[i+1] = max(dist[i], dist[i+1])

adj = set()
for k in range(n):
    adj.discard(k)
    for v in g[k]:
        if v > k:
            adj.add(v)
    print(len(adj))