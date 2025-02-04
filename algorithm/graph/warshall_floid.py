class WarshallFloid:
    INF = 1<<61

    def __init__(self,g):
        """隣接行列or頂点数"""
        if isinstance(g,int):
            g = [[self.INF] * g for _ in range(g)]
        self.n = len(g)
        self.g = g
        self.iscall = False
        for v in range(self.n):
            self.g[v][v] = 0
    
    def add_edge(self,u,v,w):
        self.g[u][v] = w
        self.g[v][u] = w
    
    def dist(self,u,v):
        if not self.iscall:
            self.warshall_floid()
        return self.g[u][v]
    
    def warshall_floid(self):
        self.iscall = True
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.g[i][j] = min(self.g[i][j],self.g[i][k]+self.g[k][j])
    
    def update(self,u,v,w):
        """辺uvの重みが小さくなる場合だけ"""
        for i in range(self.n):
            for j in range(self.n):
                self.g[i][j] = min(self.g[i][j], self.g[i][u]+w+self.g[v][j], self.g[i][v]+w+self.g[u][j])