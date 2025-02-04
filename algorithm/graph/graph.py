from collections import deque

class Graph:
    def __init__(self,graph):
        """graph: 頂点数 or 隣接リスト"""
        if isinstance(graph,int):
            graph = [[] for _ in range(graph)]
        
        self.n = len(graph)
        self.graph = graph
    
    def bfs(self,start):
        visited = [False] * self.n
        dq = deque([start])
        while dq:
            v = dq.popleft()
            if not visited[v]:
                visited[v] = True
                for nv in self.graph[v]:
                    if not visited[nv]:
                        dq.append(nv)
    
    def dfs(self,start):
        visited = [False] * self.n
        dq = deque([start])
        while dq:
            v = dq.pop()
            if not visited[v]:
                visited[v] = True
                for nv in self.graph[v]:
                    if not visited[nv]:
                        dq.append(nv)

class DirectedGraph(Graph):
    def __init__(self,graph):
        super().__init__(graph)
    
    def add_edge(self,u,v):
        self.graph[u].append(v)

class UndirectedGraph(Graph):
    def __init__(self,graph):
        super().__init__(graph)
    
    def add_edge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)