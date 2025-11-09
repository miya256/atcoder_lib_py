class SCC:
    def __init__(self, g):
        if isinstance(g, int):
            self.n = g
            self.graph = [[] for _ in range(g)]
            self.rev_graph = [[] for _ in range(g)] #逆向きの辺
        else:
            self.n = g.n
            self.graph = g.graph
            self.rev_graph = self._build(g.graph)
    
    def _build(self, graph):
        """graphクラスを受け取った場合"""
        rev_graph = [[] for _ in range(self.n)]
        for v in range(self.n):
            for nv in graph[v]:
                rev_graph[nv].append(v)
        return rev_graph
    
    def __getitem__(self,i):
        return self.graph[i]
    
    def add_edge(self,u,v):
        self.graph[u].append(v)
        self.rev_graph[v].append(u)
    
    def scc(self):
        def dfs_postorder(v):
            """帰りがけ順に番号をふる"""
            postorder = []
            stack = [v]
            while stack:
                v = stack.pop()
                if v < 0:
                    postorder.append(~v)
                    continue
                if visited[v]:
                    continue
                visited[v] = True
                stack.append(~v)
                for nv in self.graph[v]:
                    if not visited[nv]:
                        stack.append(nv)
            return postorder
        
        def dfs_scc(v):
            """強連結成分の列挙"""
            scc = []
            stack = [v]
            while stack:
                v = stack.pop()
                if visited[v]:
                    continue
                visited[v] = True
                scc.append(v)
                for nv in self.rev_graph[v]:
                    if not visited[nv]:
                        stack.append(nv)
            scc.reverse() #サイクルの逆向きに入るので戻す
            return scc
    
        visited = [False]*self.n
        postorder = []
        for v in range(self.n):
            if not visited[v]:
                postorder.extend(dfs_postorder(v))
        visited = [False]*self.n
        scc = []
        while postorder:
            v = postorder.pop()
            if not visited[v]:
                scc.append(dfs_scc(v))
        return scc
    
    def build_contracted_graph(self, scc):
        #縮約グラフの頂点vの元の頂点の集合は、scc[v]
        #つまりトポロジカル順に番号が振られる
        #縮約グラフはDAG
        scc_id = [0] * self.n #頂点vの縮約グラフでの番号
        for i in range(len(scc)):
            for v in scc[i]:
                scc_id[v] = i
        #辺を求める
        edges = set()
        for v in range(self.n):
            for nv in self.graph[v]:
                edges.add((scc_id[v], scc_id[nv]))
        return scc_id, edges