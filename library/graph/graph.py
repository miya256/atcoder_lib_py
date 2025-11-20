class Graph:
    """
    CSR形式
    buildを手動で呼び出す必要がある

    Attributes:
        n    : 頂点数
        m    : 辺数
        edges: 辺(u,v,w)
    
    Methods:
        build                : CSRの配列をつくる
        add_edge             : u -> v に重み w の 有向辺 を張る
        edge                 : id番目の辺
        neighbors            : 隣接頂点 __getitem__ に割り当て
        neighbors_with_weight: 重み付き隣接頂点 __call__ に割り当て
    """
    def __init__(self, n: int, m: int) -> None:
        self.n = n
        self.m = m
        self.edges: list[tuple[int, int, int]] = []
        self._start = [0] * (n+1)
        self._adj: list[int] | None = None
        self._weight: list[int] | None = None
    
    def __len__(self) -> int:
        """頂点数"""
        return self.n
    
    def __getitem__(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self.neighbors(v)
    
    def __call__(self, v: int) -> list[tuple[int, int]]:
        """vに隣接する頂点のリスト（重み付き）"""
        return self.neighbors_with_weight(v)
    
    def build(self) -> None:
        """グラフを作成"""
        self._adj = [0] * len(self.edges)
        self._weight = [0] * len(self.edges)
        for i in range(self.n):
            self._start[i+1] += self._start[i]
        for u, v, w in self.edges:
            self._start[u] -= 1
            self._adj[self._start[u]] = v
            self._weight[self._start[u]] = w
    
    def add_edge(self, u: int, v: int, w: int = 1) -> int:
        """u -> v に重み w の 有向辺 を張る"""
        assert 0 <= u < self.n, f"u={u} is out of range"
        assert 0 <= v < self.n, f"v={v} is out of range"
        self.edges.append((u, v, w))
        self._start[u] += 1
        return len(self.edges) - 1
    
    def edge(self, id: int) -> tuple[int, int, int]:
        """辺id"""
        assert 0 <= id < len(self.edges), f"id={id} is out of range"
        return self.edges[id]
    
    def neighbors(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        assert self._adj, "build() is not called"
        return self._adj[self._start[v]: self._start[v+1]]
    
    def neighbors_with_weight(self, v: int) -> list[tuple[int, int]]:
        """v に隣接する頂点のリスト（重み付き）"""
        assert self._adj, "build() is not called"
        return list(zip(
            self._adj[self._start[v]: self._start[v+1]],
            self._weight[self._start[v]: self._start[v+1]]
        ))
    