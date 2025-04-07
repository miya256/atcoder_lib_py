from heapq import heapify,heappush,heappop
def dijkstra(*starts,visited=None):
        """visitedはキーワード引数"""
        if visited is None:
            visited = [False]*n
        dist = [inf] * n
        hq = []
        for v in starts:
            heappush(hq,(0,v))
            dist[v] = 0
        while hq:
            d,v = heappop(hq)
            if visited[v]:
                continue
            visited[v] = True
            for nv,w in g[v]:
                if dist[nv] > d+w:
                    dist[nv] = d+w
                    heappush(hq,(dist[nv],nv))
        return dist

from heapq import heapify,heappush,heappop

class Dijkstra:
    INF = 1<<61

    def __init__(self,h,w):
        self.h = h
        self.w = w
    
    def dist(self,si,sj):
        """startからの最短距離"""
        self.prev = [[-1]*self.w for _ in range(self.h)]
        visited = [[False]*self.w for _ in range(self.h)]
        dist = [[self.INF]*self.w for _ in range(self.h)]
        hq = [(0,si,sj)]
        dist[si][sj] = 0
        while hq:
            d,i,j = heappop(hq)
            if visited[i][j]:
                continue
            visited[i][j] = True
            for di,dj in zip([0,-1,0,1],[1,0,-1,0]):
                ni, nj = i+di, j+dj
                if not(0 <= ni < self.h and 0 <= nj < self.w):
                    continue
                if dist[ni][nj] > d+1:
                    dist[ni][nj] = d+1
                    heappush(hq,(dist[ni][nj],ni,nj))
        return dist
    
    def path(self,u,v):
        """直前にuからの最短距離を求めた場合、u->vの経路を復元"""
        path = [v]
        while path[-1] != u:
            path.append(self.prev[path[-1]])
        return path


