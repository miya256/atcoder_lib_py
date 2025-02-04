class BellmanFord:
    INF = 1<<61

    def __init__(self,n,edges=[]):
        """
        n : 頂点数
        edge : [(始点,終点,重み), ...]
        """
        self.n = n
        self.edges = edges
    
    def add_edge(self,u,v,w):
        self.edges.append((u,v,w))
    
    def bellman_ford(self,start):
        d = [self.INF] * self.n
        dn = [self.INF] * self.n
        dn[start] = 0
        for _ in range(self.n):
            d = list(dn)
            for u,v,w in self.edges:
                dn[v] = min(dn[v],dn[u]+w)
        for i in range(self.n):
            if d[i] != dn[i]:
                dn[i] = -self.INF
        for _ in range(self.n):
            d = list(dn)
            for u,v,w in self.edges:
                dn[v] = min(dn[v],dn[u]+w)
        return dn
