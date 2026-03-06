from collections import deque

def bfs(starts, visited=None):
    if visited is None:
        visited = [False]*n
    dq = deque([(v,0) for v in starts])
    while dq:
        v,d = dq.popleft()
        if visited[v]:
            continue
        visited[v] = True #ここで訪れた判定
        for nv in g[v]:
            if not visited[nv]:
                dq.append((nv,d+1))

def bfs01(starts, visited=None):
    if visited is None:
        visited = [False]*n
    dq = deque([(v,0) for v in starts])
    while dq:
        v,d = dq.popleft()
        if visited[v]:
            continue
        visited[v] = True #ここで訪れた判定
        for nv,w in g[v]:
            if visited[nv]:
                continue
            if w == 0:
                dq.appendleft((nv,d))
            else:
                dq.append((nv,d+w))

def bfs_grid(h, w, starts, visited=None):
    if visited is None:
        visited = [[False]*w for _ in range(h)]
    dq = deque([(i,j,0) for i,j in starts])
    while dq:
        i,j,d = dq.popleft()
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