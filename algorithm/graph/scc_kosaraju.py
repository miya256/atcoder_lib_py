import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class SCC:
    def __init__(self,n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self,u,v):
        """uからvに辺を張る"""
        self.g[u].append(v)

    def _dfs1(self,v):
        self.visited[v] = True
        for nv in self.g[v]:
            self.backg[nv].append(v)
            if self.visited[nv]:
                continue
            self._dfs1(nv)
        self.stack.append(v)

    def _dfs2(self,v):
        self.visited[v] = True
        self.res[-1].append(v)
        for nv in self.backg[v]:
            if self.visited[nv]:
                continue
            self._dfs2(nv)

    def scc(self):
        self.backg = [[] for _ in range(self.n)]
        self.stack = []
        self.visited = [False]*self.n
        for i in range(self.n):
            if self.visited[i]:
                continue
            self._dfs1(i)
        self.res = []
        self.visited = [False]*self.n
        for _ in range(self.n):
            v = self.stack.pop()
            if self.visited[v]:
                continue
            self.res.append([])
            self._dfs2(v)
        return self.res
