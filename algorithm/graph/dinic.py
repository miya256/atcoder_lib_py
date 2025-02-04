#最大流、最小カット、最大二部マッチング
from collections import deque
class Dinic:
    def __init__(self,n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.dist = [-1]*n

    def add_edge(self,fr,to,cap):
        """辺のmerge"""
        forward = [to,cap,None]
        forward[2] = backward = [fr,0,forward]
        self.g[fr].append(forward)
        self.g[to].append(backward)

    def bfs(self,s,t):
        """sからt"""
        self.dist = [-1]*self.n
        dq = deque([s])
        self.dist[s] = 0
        while dq:
            v = dq.popleft()
            for nv,cap,_ in self.g[v]:
                if cap and self.dist[nv] == -1:
                    self.dist[nv] = self.dist[v] + 1
                    dq.append(nv)
        return self.dist[t] != -1

    def dfs(self,s,t,f):
        """s:始点,t:終点,f:流量"""
        if s == t:
            return f
        for e in self.it[s]:
            nv,cap,rev = e
            if cap and self.dist[s] < self.dist[nv]:
                flow = self.dfs(nv,t,min(f,cap))
                if flow:
                    e[1] -= flow
                    rev[1] += flow
                    return flow
        return 0

    def getMaxFlow(self,s,t):
        flow = 0
        while self.bfs(s,t):
            *self.it, _ = map(iter,self.g)
            f = float('inf')
            while f:
                f = self.dfs(s,t,float('inf'))
                flow += f
        return flow

#-----------------------------------------
#最大二部マッチングでグラフが与えられたとき
#最大流のグラフをつくる
def dfs(v,visited,colors):
    visited[v] = True
    for nv in g[v]:
        if visited[nv]:
            continue
        colors[nv] = colors[v] ^1
        dfs(nv,visited,colors)

def getColor(g,n):
    visited = [False]*n
    colors = [-1]*n
    for v in range(n):
        if colors[v] != -1:
            continue
        colors[v] = 0
        dfs(v,visited,colors)
    return colors

def createGraph(g):
    n = len(g)
    colors = getColor(g,n)
    ng = Dinic(n+2)
    for i,v in enumerate(g):
        if colors[i]:
            continue
        for j in v:
            ng.add_edge(i,j,1)
    for i,c in enumerate(colors):
        if c:
            ng.add_edge(i,n+1,1)
        else:
            ng.add_edge(n,i,1)
    return ng
