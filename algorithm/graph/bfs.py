from collections import deque

class BFS:
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
    
    def bfs(self,starts): #始点が1つの場合も、長さ1の配列にして渡す
        dq = deque(starts)
        while dq:
            v = dq.popleft()
            if not self.visited[v]:
                self.visited[v] = True #ここで訪れた判定。訪れたくないなら、そもそもキューにいれない
                for nv in self.graph[v]:
                    if not self.visited[nv]:
                        dq.append(nv)

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