class WarshallFloid(Graph):
    def __init__(self, n: int) -> None:
        super().__init__(n)
        inf = 1<<61
        self._dist = [[inf] * n for _ in range(n)]
        self._called = False
    
    def add_edge(self, u: int, v: int, w: int) -> int:
        """u -> v へ重み w の 有向辺 を張る"""
        self._dist[u][v] = min(self._dist[u][v], w)
        return super().add_edge(u, v, w)
    
    def dist(self, u: int, v: int) -> int:
        """u -> v の距離"""
        assert self._called, "buildメソッドを実行してください"
        return self._dist[u][v]
    
    def build(self) -> None:
        """行列を作成"""
        self._called = True
        for i in range(self._n):
            self._dist[i][i] = 0

        for k in range(self._n):
            for i in range(self._n):
                for j in range(self._n):
                    self._dist[i][j] = min(self._dist[i][j], self._dist[i][k] + self._dist[k][j])
    
    def update(self, u: int, v: int, w: int) -> None:
        """
        辺uvの重みをwにする。辺の重みが小さくなる場合だけ
        ※無向の場合は、v->uも 呼ぶ必要がある
        """
        for i in range(self._n):
            for j in range(self._n):
                self._dist[i][j] = min(self._dist[i][j], self._dist[i][u] + w + self._dist[v][j])