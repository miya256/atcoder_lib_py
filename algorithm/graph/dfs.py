import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")
from collections import deque

def dfs(*starts,visited=None):
    """visitedはキーワード引数"""
    if visited is None:
        visited = [False]*n
    dq = deque([(v,0) for v in starts])
    while dq:
        v,d = dq.pop()
        if visited[v]:
            continue
        visited[v] = True #ここで訪れた判定
        for nv,w in g[v]:
            if visited[nv]:
                continue
            dq.append((nv,d+w))

def dfs(v):
    visited_in[v] = True
    for nv in g[v]:
        if visited_in[nv]:
            continue
        dfs(nv)
    visited_out[v] = True

#木のdfs
def dfs(v,par=-1):
    for nv in g[v]:
        if nv != par:
            dfs(nv,v)

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
