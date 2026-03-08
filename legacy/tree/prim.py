from heapq import heapify,heappush,heappop

class Prim:
    def __init__(self,graph):
        if isinstance(graph,int):
            graph = [[] for _ in range(graph)]
        
        self.n = len(graph)
        self.graph = graph
    
    def add_edge(self,u,v,w):
        self.graph[u].append((v,w))
        self.graph[v].append((u,w))
    
    def prim(self,start):
        visited = [False]*self.n
        node_count = 0
        weight = 0
        hq = [(0,start)]
        while node_count < self.n:
            w,v = heappop(hq)
            if visited[v]:
                continue
            visited[v] = True
            weight += w
            node_count += 1
            for nv,w in self.graph[v]:
                if visited[nv]:
                    continue
                heappush(hq,(w,nv))
        return weight