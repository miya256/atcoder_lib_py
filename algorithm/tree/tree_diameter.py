class Diameter:
    INF = 1<<61

    def __init__(self,n):
        self.n = n
        self.graph = [[] for _ in range(n)]
    
    def add_edge(self,u,v,w=1):
        self.graph[u].append((v,w))
        self.graph[v].append((u,w))
    
    def _dfs(self, v, dist=None):
        """distを指定すればvからの距離、そうでなければ直径と端点"""
        stack = [(v,-1,0)]
        end, diameter = -1, 0
        while stack:
            v, par, d = stack.pop()

            if dist is not None:
                dist[v] = d

            if diameter < d:
                diameter = d
                end = v

            for nv,w in self.graph[v]:
                if nv != par:
                    stack.append((nv, v, d+w))
        
        return diameter, end
    
    def diameter(self):
        _, end1 = self._dfs(0)
        diameter, end2 = self._dfs(end1)
        return diameter, end1, end2
    
    def find_farthest_dist(self):
        """すべてのvについて、vから最も遠い点までの距離を求める"""
        _, end1, end2 = self.diameter()
        dist1 = [self.INF] * self.n
        dist2 = [self.INF] * self.n
        self._dfs(end1, dist1)
        self._dfs(end2, dist2)
        return [max(d1, d2) for d1, d2 in zip(dist1, dist2)]