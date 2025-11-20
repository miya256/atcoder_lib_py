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
        self.edges.append((u, v, w))
        self._start[u] += 1
        return len(self.edges) - 1
    
    def edge(self, id: int) -> tuple[int, int, int]:
        """辺id"""
        return self.edges[id]
    
    def neighbors(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self._adj[self._start[v]: self._start[v+1]]
    
    def neighbors_with_weight(self, v: int) -> list[tuple[int, int]]:
        """v に隣接する頂点のリスト（重み付き）"""
        return list(zip(self._adj[self._start[v]: self._start[v+1]], self._weight[self._start[v]: self._start[v+1]]))

class SCC(Graph):
    def __init__(self, n: int, m: int) -> None:
        super().__init__(n, m)
        self._rev_graph = Graph(n, m)
    
    def add_edge(self, u: int, v: int) -> int:
        self._rev_graph.add_edge(v, u)
        return super().add_edge(u, v)
    
    def scc(self) -> list[list[int]]:
        def dfs_postorder(v: int) -> list[int]:
            """帰りがけ順に番号をふる"""
            postorder = []
            stack = [v]
            while stack:
                u = stack.pop()
                if u < 0:
                    postorder.append(~u)
                    continue
                if visited[u]:
                    continue
                visited[u] = True
                stack.append(~u)
                for v in self[u]:
                    if not visited[v]:
                        stack.append(v)
            return postorder
        
        def dfs_scc(v: int) -> list[int]:
            """強連結成分の列挙"""
            scc = []
            stack = [v]
            while stack:
                u = stack.pop()
                if visited[u]:
                    continue
                visited[u] = True
                scc.append(u)
                for v in self._rev_graph[u]:
                    if not visited[v]:
                        stack.append(v)
            scc.reverse() #サイクルの逆向きに入るので戻す
            return scc

        super().build()
        self._rev_graph.build()
        visited = [False] * self.n
        postorder = []
        for v in range(self.n):
            if not visited[v]:
                postorder.extend(dfs_postorder(v))

        visited = [False] * self.n
        scc = []
        while postorder:
            v = postorder.pop()
            if not visited[v]:
                scc.append(dfs_scc(v))
        return scc
    
    def build_contracted_graph(self, scc: list[list[int]]) -> tuple[list[int], list[tuple[int, int]]]:
        """
        縮約グラフ
        縮約グラフの頂点vの元の頂点の集合は、scc[v]
        つまりトポロジカル順に番号が振られる
        縮約グラフはDAG
        """
        scc_id = [0] * self.n #頂点vの縮約グラフでの番号
        for i in range(len(scc)):
            for v in scc[i]:
                scc_id[v] = i
        edges = set()
        for u in range(self.n):
            for v in self[u]:
                if scc_id[u] != scc_id[v]:
                    edges.add((scc_id[u], scc_id[v]))
        return scc_id, list(edges)

n,m = map(int,input().split())
g = SCC(n,m)
for _ in range(m):
    a,b = map(int,input().split())
    g.add_edge(a, b)

scc = g.scc()
print(len(scc))
for group in scc:
    print(len(group), *group)