import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class DirectedGraph:
    def __init__(self,g):
        """頂点数 or 隣接リスト"""
        if isinstance(g,int):
            g = [[] for _ in range(g)]
        self.n = len(g)
        self.graph = g
        self.visited = []
        self.array = []
    
    def __getitem__(self,i):
        return self.graph[i]
    
    def add_edge(self,u,v):
        self.graph[u].append(v)
    
    def _dfs(self,v):
        self.visited[v] = True
        for nv in self.graph[v]:
            if not self.visited[nv]:
                self._dfs(nv)
        self.array.append(v)
    
    def topologicalsort(self):
        self.array = []
        self.visited = [False]*self.n
        for v in range(self.n):
            if not self.visited[v]:
                self._dfs(v)
        return self.array[::-1]