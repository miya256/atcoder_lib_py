from collections import deque

def dfs(graph: Graph, starts: list[int]) -> None:
    dq = deque([(v, 0) for v in starts])
    visited = [False] * graph.n
    while dq:
        u, d = dq.pop()
        if visited[u]:
            continue
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dq.append((v, d+1))


def dfs(graph: Graph, u: int):
    #in vertex u
    for v in graph[u]:
        if "visited":
            continue
        dfs(graph, v)
    #out vertex u