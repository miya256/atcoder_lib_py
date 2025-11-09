#Kahn's algorithmという入次数が0のやつから選ぶのもある
#辞書順の場合はKahnでやる

class TopologicalSort:
    UNVISITED = -1 #未訪問
    VISITING = 0 #行きがけで訪れた
    VISITED = 1 #帰りがけで訪れた

    def __init__(self, g):
        if isinstance(g, int):
            self.n = g
            self.graph = [[] for _ in range(g)]
        else:
            self.n = g.n
            self.graph = g.graph
    
    def __getitem__(self, i):
        return self.graph[i]
    
    def add_edge(self, u, v):
        """uからvへの**有向辺**を張る"""
        self.graph[u].append(v)
    
    def topologicalsort_dfs(self):
        """トポロジカルソート。サイクルがあったらNoneを返す"""
        def dfs(v):
            stack = [v]
            while stack:
                v = stack.pop()
                if v >= 0:
                    if visit_state[v] == self.VISITING:
                        return False
                    if visit_state[v] == self.VISITED:
                        continue
                    visit_state[v] = self.VISITING
                    stack.append(~v) #帰り用
                    for nv in self.graph[v]:
                        if visit_state[nv] != self.VISITED:
                            stack.append(nv)
                else:
                    v = ~v
                    visit_state[v] = self.VISITED
                    postorder.append(v)
            return True
    
        postorder = []
        visit_state = [self.UNVISITED for _ in range(self.n)]
        for v in range(self.n):
            if visit_state[v] == self.UNVISITED:
                is_dag = dfs(v)
                if not is_dag:
                    return None
        return postorder[::-1]
    
    def topologicalsort_kahn(self):
        """入次数が0のやつから順に"""
        def calc_in_degree():
            in_degree = [0] * self.n
            for v in range(self.n):
                for nv in self.graph[v]:
                    in_degree[nv] += 1
            return in_degree
    
        in_degree = calc_in_degree()
        zero_in = [v for v in range(self.n) if in_degree[v] == 0]

        order = []
        while zero_in:
            v = zero_in.pop()
            order.append(v)
            for nv in self.graph[v]:
                in_degree[nv] -= 1
                if in_degree[nv] == 0:
                    zero_in.append(nv)
        
        return order if len(order) == self.n else None