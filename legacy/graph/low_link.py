class LowLink:
    def __init__(self, g):
        if isinstance(g, int):
            self.n = g
            self.graph = [[] for _ in range(g)]
        else:
            self.n = g.n
            self.graph = g.graph
        self.bridge = []
        self.articulation_points = set()
    
    def __getitem__(self, i):
        return self.graph[i]
    
    def add_edge(self, u, v):
        """uからvへの**有向辺**を張る"""
        self.graph[u].append(v)
    
    def _dfs(self, v, visited, ord, low, k):
        stack = [(v, v)] #rootのparを-1にすると悪さをするのでvにしている
        root = v
        child_count = 0
        while stack:
            v, par = stack.pop()
            if v >= 0:
                if visited[v]: #par -> vが後退辺なら
                    low[par] = min(low[par], ord[v])
                    continue
                visited[v] = True
                ord[v] = low[v] = k
                k += 1
                if par == root:
                    child_count += 1
                stack.append((~v, par))
                for nv in self.graph[v]:
                    if nv != par:
                        stack.append((nv, v))
            else:
                v = ~v
                low[par] = min(low[par], low[v])
                if par != root and ord[par] <= low[v]:
                    self.articulation_points.add(par)
                if ord[par] < low[v]:
                    self.bridge.append((par, v))
        if child_count >= 2:
            self.articulation_points.add(root)
        return k

    def build(self):
        visited = [False] * self.n
        ord = [0] * self.n
        low = [0] * self.n
        k = 0
        for v in range(self.n):
            if not visited[v]:
                k = self._dfs(v, visited, ord, low, k)
        return ord, low