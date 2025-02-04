import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")
from collections import deque

class LowLink:
    def __init__(self,n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = []
        self.articulation_points = set()
        self.bridges = set()
        self.ord = [-1] * n
        self.low = [-1] * n
    
    def add_edge(self,u,v):
        self.graph[u].append((len(self.edges),v))
        self.graph[v].append((len(self.edges),u))
        self.edges.append((min(u,v),max(u,v)))
    
    def get_articulation_points(self):
        """関節点をあげる"""
        return sorted(list(self.articulation_points))
    
    def get_bridges(self):
        """(辺番号,(頂点、頂点))"""
        return sorted[self.bridge]
    
    def _dfs(self,visited,k,v,pre=-1):
        visited[v] = True
        self.ord[v] = k
        self.low[v] = k
        cnt = 0#関節点を調べるために子の数をカウント
        for i,nv in self.graph[v]:
            if not visited[nv]:
                cnt += 1
                k = self._dfs(visited,k+1,nv,v)
                self.low[v] = min(self.low[v],self.low[nv])
                if pre != -1 and self.ord[v] <= self.low[nv]:
                    self.articulation_points.add(v)
                if self.ord[v] < self.low[nv]:
                    self.bridges.add((i,(min(v,nv),max(v,nv))))
            elif nv != pre:
                self.low[v] = min(self.low[v],self.ord[nv])
        if pre == -1 and cnt >= 2:
            self.articulation_points.add(v)
        return k

    def lowlink(self):
        visited = [False] * self.n
        k = -1
        for v in range(self.n):
            if not visited[v]:
                k = self._dfs(visited,k+1,v)

#二重辺連結成分分解
class BCC(LowLink):
    def __init__(self,n):
        super().__init__(n)
        self.n = n
        self.groups = []
        self.group_num = [-1] * n
        self.tree = []
    
    def _dfs_bcc(self,visited,v):
        visited[v] = True
        self.groups[-1].append(v)
        self.group_num[v] = len(self.groups)-1
        for i,nv in self.graph[v]:
            if not visited[nv] and (i,(min(v,nv),max(v,nv))) not in self.bridges:
                self._dfs_bcc(visited,nv)
    
    def bcc(self):
        """二重辺連結成分分解"""
        self.groups = []
        self.group_num = [-1] * n
        self.lowlink()
        visited = [False] * self.n
        for v in range(self.n):
            if not visited[v]:
                self.groups.append([])
                self._dfs_bcc(visited,v)
        return self.groups,self.group_num
    
    def make_tree(self):
        """縮約木の構築"""
        if not self.groups:
            self.bcc()
        self.tree = [[] for _ in range(len(self.groups))]
        for i,(u,v) in self.bridges:
            self.tree[self.group_num[u]].append(self.group_num[v])
            self.tree[self.group_num[v]].append(self.group_num[u])
        return self.tree

#二重頂点連結成分分解


n = 10
edges = [(0,1),(1,2),(1,3),(2,3),(3,4),(4,5),(4,6),(6,7),(6,8),(7,9),(8,9)]

g = BCC(n)
for u,v in edges:
    g.add_edge(u,v)
groups,num = g.bcc()
tree = g.make_tree()
print(groups)
print(num)
print(tree)
