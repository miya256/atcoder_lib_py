from collections import deque

def bfs(graph: Graph, starts: list[int]) -> None:
    """重みが01のとき"""
    dq = deque([(v, 0) for v in starts])
    visited = [False] * graph.n
    while dq:
        u, d = dq.popleft()
        if visited[u]:
            continue
        visited[u] = True
        for v, w in graph(u):
            if visited[v]:
                continue
            if w == 0:
                dq.appendleft((v, d))
            else:
                dq.append((v, d+w))