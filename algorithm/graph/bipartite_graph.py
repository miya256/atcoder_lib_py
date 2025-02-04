import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class Graph:
    def __init__(self,g):
        if isinstance(g,int):
            g = [[] for _ in range(g)]
        self.n = len(g)
        self.graph = g
        self.color = [-1] * self.n

    def __getitem__(self,i):
        return self.graph[i]

    def add_edge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def dfs(self,v):
        for nv in self[v]:
            if self.color[nv] == self.color[v]:
                return False
            if self.color[nv] != -1:
                continue
            self.color[nv] = self.color[v] ^ 1
            if not self.dfs(nv):
                return False
        return True
    
    def isBipartite(self):
        for v in range(self.n):
            if self.color[v] != -1:
                continue
            self.color[v] = 0
            if not self.dfs(v):
                return False
        return True
