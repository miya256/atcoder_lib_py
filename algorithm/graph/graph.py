from collections import deque,defaultdict,Counter
class Graph:
    INF = 1<<61

    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def __getitem__(self, i):
        return self.graph[i]

    def add_edge(self, u, v):
        """uからvへの**有向辺**を張る"""
        self.graph[u].append(v)

    def bfs(self, *starts, visited=None):
        """visitedはキーワード引数"""
        if visited is None:
            visited = [False] * self.n
        dist = [self.INF] * self.n
        dq = deque([(v, 0) for v in starts])
        while dq:
            v, d = dq.popleft()
            if visited[v]:
                continue
            visited[v] = True #ここで訪れた判定
            dist[v] = d
            for nv in self.graph[v]:
                if not visited[nv]:
                    dq.append((nv, d+1))
        return dist

    def dfs(self, *starts, visited=None):
        """visitedはキーワード引数"""
        if visited is None:
            visited = [False] * self.n
        dq = deque([(v, 0) for v in starts])
        while dq:
            v, d = dq.pop()
            if visited[v]:
                continue
            visited[v] = True #ここで訪れた判定
            for nv in self.graph[v]:
                if not visited[nv]:
                    dq.append((nv, d+1))


from heapq import heapify,heappush,heappop
from collections import deque,defaultdict,Counter
class WeightedGraph:
    INF = 1<<61

    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
    
    def __getitem__(self, i):
        return self.graph[i]
    
    def add_edge(self, u, v, w):
        """uからvへ重みwの**有向辺**を張る"""
        self.graph[u].append((v, w))
    
    def dijkstra(self, *starts, visited=None):
        """visitedはキーワード引数"""
        if visited is None:
            visited = [False]*self.n
        dist = [self.INF] * self.n
        hq = []
        for v in starts:
            heappush(hq,(0, v))
            dist[v] = 0
        while hq:
            d,v = heappop(hq)
            if visited[v]:
                continue
            visited[v] = True
            for nv, w in self.graph[v]:
                if dist[nv] > d+w:
                    dist[nv] = d+w
                    heappush(hq, (dist[nv], nv))
        return dist
    
    def bfs01(self, *starts, visited=None):
        """visitedはキーワード引数"""
        if visited is None:
            visited = [False] * self.n
        dq = deque([(v, 0) for v in starts])
        while dq:
            v, d = dq.popleft()
            if visited[v]:
                continue
            visited[v] = True #ここで訪れた判定
            for nv, w in self.graph[v]:
                if visited[nv]:
                    continue
                if w == 0:
                    dq.appendleft((nv, d))
                else:
                    dq.append((nv, d+w))