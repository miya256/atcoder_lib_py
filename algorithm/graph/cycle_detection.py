import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class CycleDetection:
    def __init__(self,graph):
        """隣接リストor頂点数"""
        if isinstance(graph,int):
            graph = [[] for _ in range(graph)]
        self.n = len(graph)
        self.graph = graph
        self.forward = [False] * self.n
        self.backward = [False] * self.n
        self.path = []
    
    def add_edge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def dfs(self,v,prev=-1):
        self.forward[v] = True
        for nv in self.graph[v]:
            if nv != prev and self.forward[nv] and not self.backward[nv]:
                self.path.append(nv)
                return True
            elif self.forward[nv]:
                continue
            if self.dfs(nv,v):
                if len(self.path) <= 1 or self.path[0] != self.path[-1]:
                    self.path.append(nv)
                return True
        self.backward[v] = True
        return False
    
    def hasCycle(self):
        self.forward = [False] * self.n
        self.backward = [False] * self.n
        self.path = []
        for v in range(self.n):
            if self.forward[v]:
                continue
            if self.dfs(v):
                return True
        return False
    
    def getPath(self):
        """hasCycleして見つけたサイクル"""
        return self.path