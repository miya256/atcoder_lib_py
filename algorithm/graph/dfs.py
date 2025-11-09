import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")
from collections import deque

def dfs(starts,visited=None):
    if visited is None:
        visited = [False]*n
    dq = deque([(v,0) for v in starts])
    while dq:
        v,d = dq.pop()
        if visited[v]:
            continue
        visited[v] = True #ここで訪れた判定
        for nv in g[v]:
            if visited[nv]:
                continue
            dq.append((nv,d+1))

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

def dfs_grid(h, w, starts, visited=None):
    if visited is None:
        visited = [[False]*w for _ in range(h)]
    dq = deque([(i,j,0) for i,j in starts])
    while dq:
        i,j,d = dq.pop()
        if visited[i][j]:
            continue
        visited[i][j] = True
        for di,dj in (-1,0), (1,0), (0,-1), (0,1):
            ni, nj = i+di, j+dj
            if not(0 <= ni < h and 0 <= nj < w):
                continue
            if visited[ni][nj]:
                continue
            dq.append((ni,nj,d+1))