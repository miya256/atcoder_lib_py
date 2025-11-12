from collections import deque

def bfs(graph: Graph, starts: list[int]) -> None:
    dq = deque([(v, 0) for v in starts])
    visited = [False] * graph.n
    while dq:
        u, d = dq.popleft()
        if visited[u]:
            continue
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dq.append((v, d+1))