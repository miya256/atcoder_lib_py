import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")
from collections import deque

class DFS:
    def __init__(self,g):
        """隣接リストor頂点数"""
        if isinstance(g,int):
            g = [[] for _ in range(g)]
        self.n = len(g)
        self.graph = g
        self.visited = [False] * self.n #初期化するべき時に初期化する
    
    def add_edge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def dfs(self,starts): #始点が1つの場合も、長さ1の配列にして渡す
        dq = deque(starts)
        while dq:
            v = dq.pop()
            if not self.visited[v]:
                self.visited[v] = True #ここで訪れた判定。訪れたくないなら、そもそもキューにいれない
                for nv in self.graph[v]:
                    if not self.visited[nv]:
                        dq.append(nv)
def dfs(v):
    visited_in[v] = True
    for nv in g[v]:
        if visited_in[nv]:
            continue
        dfs(nv)
    visited_out[v] = True


#木のdfs
def dfs(v,pre=-1):
    for nv in g[v]:
        if nv == pre:
            continue
        dfs(nv,v)

#非再帰
def dfs(starts):
    dq = deque(starts)
    while dq:
        v = dq.pop()
        if not visited[v]:
            visited[v] = True
            for nv in g[v]:
                if not visited[nv]:
                    dq.append(nv)

class DFS:
    def __init__(self,grid):
        self.h = len(grid)
        self.w = len(grid[0])
        self.grid = grid
        self.visited = [[False] * self.w for _ in range(self.h)]
    
    def dfs(self,starts):
        dq = deque(starts)
        while dq:
            i,j = dq.pop()
            if not self.visited[i][j]:
                self.visited[i][j] = True
                for di,dj in zip([0,-1,0,1],[1,0,-1,0]):
                    ni, nj = i+di, j+dj
                    if not(0 <= ni < self.h and 0 <= nj < self.w):
                        continue
                    if self.visited[ni][nj]:
                        continue
                    dq.append((ni,nj))

def dfs(starts):
    dq = deque(starts)
    while dq:
        i,j = dq.pop()
        if not visited[i][j]:
            visited[i][j] = True
            for di,dj in zip([0,-1,0,1],[1,0,-1,0]):
                ni, nj = i+di, j+dj
                if not(0 <= ni < h and 0 <= nj < w):
                    continue
                if visited[ni][nj]:
                    continue
                dq.append((ni,nj))
