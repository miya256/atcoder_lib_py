class WarshallFloid:
    INF = 1<<61

    def __init__(self,n):
        self.n = n #頂点数
        self.g = [[self.INF]*n for _ in range(n)]
        self.edges = []
        self.called = False #buildが呼ばれたか
    
    def add_edge(self,u,v,w):
        """uからvへ重みwの**有向辺**を張る"""
        self.g[u][v] = min(self.g[u][v],w)
    
    def dist(self,u,v):
        assert self.called, "buildメソッドを実行してください"
        return self.g[u][v]
    
    def build(self):
        self.called = True
        for i in range(self.n):
            self.g[i][i] = 0
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    self.g[i][j] = min(self.g[i][j],self.g[i][k]+self.g[k][j])
    
    def update(self, u, v, w):
        """辺uvの重みをwにする。辺の重みが小さくなる場合だけ"""
        for i in range(self.n):
            for j in range(self.n):
                self.g[i][j] = min(self.g[i][j], self.g[i][u] + w + self.g[v][j], self.g[i][v] + w + self.g[u][j])