class Graph:
    class Edge:
        """
        Attributes:
            id: 辺の番号
            u : 始点
            v : 終点
            w : 辺の重み
        """
        def __init__(self, id: int, u: int, v: int, w: int) -> None:
            self.id = id
            self.u = u
            self.v = v
            self.w = w
        
        def __repr__(self):
            return f"Edge({self.id}, {self.u} -> {self.v}, {self.w})"

    def __init__(self, n: int) -> None:
        self._n = n
        self._edges: list[Graph.Edge] = []
        self._adj: list[list[Graph.Edge]] = [[] for _ in range(n)]
    
    def __len__(self) -> int:
        """頂点数"""
        return self._n
    
    def __getitem__(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self.neighbors(v)
    
    def __call__(self, v: int) -> list[tuple[int, int]]:
        """vに隣接する頂点のリスト（重み付き）"""
        return self.neighbors_with_weight(v)
    
    def add_edge(self, u: int, v: int, w: int = 1) -> int:
        """u -> v に重み w の 有向辺 を張る"""
        edge = Graph.Edge(len(self._edges), u, v, w)
        self._edges.append(edge)
        self._adj[u].append(edge)
        return edge.id
    
    def edge(self, id: int) -> Edge:
        """辺id"""
        return self._edges[id]
    
    def neighbors(self, v: int) -> list[int]:
        """v に隣接する頂点のリスト"""
        return [edge.v for edge in self._adj[v]]
    
    def neighbors_with_weight(self, v: int) -> list[tuple[int, int]]:
        """v に隣接する頂点のリスト（重み付き）"""
        return [(edge.v, edge.w) for edge in self._adj[v]]
    
    @property
    def n(self) -> int:
        """頂点数"""
        return self._n
    
    @property
    def edges(self) -> list[tuple[int, int, int]]:
        """辺のリスト（tuple）"""
        return [(edge.u, edge.v, edge.w) for edge in self._edges]