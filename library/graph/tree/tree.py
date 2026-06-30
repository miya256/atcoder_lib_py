class Tree:
    """
    CSR形式
    n-1辺張ったら自動build

    Attributes:
        n    : 頂点数
        edges: 辺(u,v,w)
        子クラスからも参照するからpublic

    Methods:
        build()                 : CSRの配列をつくる
        add_edge(u, v, w=1)     : u -> v に重み w の 有向辺 を張る
        edge(i)                 : i番目の辺
        neighbors(v)            : 隣接頂点 __getitem__ に割り当て
        neighbors_with_weight(v): 重み付き隣接頂点 __call__ に割り当て
    """

    def __init__(self, n: int):
        self.n = n
        self.edges: list[tuple[int, int, int]] = []
        self._ptr = [0] * (n + 1)
        self._adj: list[int] = []
        self._weight: list[int] = []

    def __len__(self) -> int:
        """頂点数"""
        return self.n

    def __getitem__(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self.neighbors(v)

    def __call__(self, v: int) -> list[tuple[int, int]]:
        """vに隣接する頂点のリスト（重み付き）"""
        return self.neighbors_with_weight(v)

    def _build_csr(self) -> None:
        """木を作成"""
        self._adj = [0] * len(self.edges)
        self._weight = [0] * len(self.edges)
        for i in range(self.n):
            self._ptr[i + 1] += self._ptr[i]
        for u, v, w in self.edges:
            self._ptr[u] -= 1
            self._adj[self._ptr[u]] = v
            self._weight[self._ptr[u]] = w

    def add_edge(self, u: int, v: int, w: int = 1) -> None:
        """u -> v に重み w の 無向辺 を張る"""
        assert 0 <= u < self.n, f"u={u} is out of range"
        assert 0 <= v < self.n, f"v={v} is out of range"
        self.edges.append((u, v, w))
        self.edges.append((v, u, w))
        self._ptr[u] += 1
        self._ptr[v] += 1

        if len(self.edges) >= 2 * (self.n - 1):
            self._build_csr()

    def neighbors(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self._adj[self._ptr[v] : self._ptr[v + 1]]

    def neighbors_with_weight(self, v: int) -> list[tuple[int, int]]:
        """v に隣接する頂点のリスト（重み付き）"""
        return list(
            zip(
                self._adj[self._ptr[v] : self._ptr[v + 1]],
                self._weight[self._ptr[v] : self._ptr[v + 1]],
            )
        )
