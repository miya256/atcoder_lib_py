from heapq import heapify,heappush,heappop

class Dijkstra:
    INF = 1<<61

    def __init__(self,g):
        """隣接リストor頂点数"""
        if isinstance(g,int):
            g = [[] for _ in range(g)]
        self.n = len(g)
        self.g = g
        self.prev = [-1] * self.n
    
    def add_edge(self,u,v,w,isDirected=None):
        assert isDirected is not None, "有向辺かどうかを確かめてください"
        self.g[u].append((v,w))
        if not isDirected:
            self.g[v].append((u,w))
    
    def dijkstra(self,start:int):
        """startからの最短距離"""
        self.prev = [-1] * self.n
        visited = [False] * self.n
        dist = [self.INF] * self.n
        hq = [(0,start,-1)]
        dist[start] = 0
        while hq:
            d,v,prev = heappop(hq)
            if visited[v]:
                continue
            visited[v] = True
            self.prev[v] = prev
            for nv,w in self.g[v]:
                if dist[nv] > d+w:
                    dist[nv] = d+w
                    heappush(hq,(dist[nv],nv,v))
        return dist
    
    def get_path(self,u,v):
        """直前にuからの最短距離を求めた場合、u->vの経路を復元"""
        path = [v]
        while path[-1] != u:
            path.append(self.prev[path[-1]])
        return path[::-1]


class Dijkstra:
    INF = 1<<61

    def __init__(self,h,w):
        self.h = h
        self.w = w
    
    def dijkstra(self,si,sj):
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
    
    def get_path(self,u,v):
        """直前にuからの最短距離を求めた場合、u->vの経路を復元"""
        path = [v]
        while path[-1] != u:
            path.append(self.prev[path[-1]])
        return path


