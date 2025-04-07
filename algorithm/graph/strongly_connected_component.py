class StronglyConnectedComponent:
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
    
    def _dfs_postorder(self,v,visited):
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
    
    def _dfs_scc(self,v,visited):
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
    
    def scc(self):
        visited = [False]*self.n
        postorder = []
        for v in range(self.n):
            if not visited[v]:
                postorder.extend(self._dfs_postorder(v,visited))
        visited = [False]*self.n
        scc = []
        while postorder:
            v = postorder.pop()
            if not visited[v]:
                scc.append(self._dfs_scc(v,visited))
        return scc