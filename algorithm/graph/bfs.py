from collections import deque

def bfs(*starts,visited=None):
    """visitedはキーワード引数"""
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

def bfs01(*starts,visited=None):
    """visitedはキーワード引数"""
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

#Grid
from collections import deque
class BFS:
    def __init__(self,grid):
        self.h = len(grid)
        self.w = len(grid[0])
        self.grid = grid
        self.visited = [[False] * self.w for _ in range(self.h)]
    
    def bfs(self,starts):
        dq = deque(starts)
        while dq:
            i,j = dq.popleft()
            if not self.visited[i][j]:
                self.visited[i][j] = True
                for di,dj in zip([0,-1,0,1],[1,0,-1,0]):
                    ni, nj = i+di, j+dj
                    if not(0 <= ni < self.h and 0 <= nj < self.w):
                        continue
                    if self.visited[ni][nj]:
                        continue
                    #他にも壁とかがあれば条件を追加する
                    dq.append((ni,nj))