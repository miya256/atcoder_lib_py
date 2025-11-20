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

        self.build()
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