class UnionFind:
    def __init__(self,n):
        """
        n: 頂点数
        parent: 親
        size: 頂点iが属する連結成分の頂点数
        """
        self.n = n
        self.parent = [i for i in range(n)]
        self.size = [1]*n
    
    def leader(self,v):
        """頂点vの属する連結成分の根"""
        if v != self.parent[v]:
            stack = []
            while v != self.parent[v]:
                stack.append(v)
                v = self.parent[v]
            while stack:
                self.parent[stack.pop()] = v
        return v
    
    def merge(self,u,v):
        """連結した後の根を返す"""
        ru = self.leader(u)
        rv = self.leader(v)
        if ru == rv:
            return False
        if self.size[ru] < self.size[rv]:
            ru,rv = rv,ru
        #ruにrvをmerge
        self.parent[rv] = ru
        self.size[ru] += self.size[rv]
        return True
    
    def same(self,u,v):
        return self.leader(u) == self.leader(v)
    
    def get_size(self,v):
        return self.size[self.leader[v]]
    
    def roots(self):
        return [i for i,v in enumerate(self.parent) if i == v]
    
    def members(self,v):
        rv = self.leader(v)
        return [i for i in range(self.n) if self.leader(i) == rv]
    
    def groups(self):
        res = {i:list() for i in self.roots()}
        for i in range(self.n):
            res[self.leader(i)].append(i)
        return res
    
    def count_connected_components(self):
        return len(self.roots())
    
    def __str__(self):
        return f'{self.groups()}'

class Kruskal:
    def __init__(self,n):
        self.n = n
        self.uf = UnionFind(n)
        self.edges = []
    
    def add_edge(self,u,v,w):
        self.edges.append((u,v,w))
    
    def kruskal(self):
        weight = 0
        self.edges.sort(key = lambda x:x[2])
        for u,v,w in self.edges:
            if self.uf.same(u,v):
                continue
            weight += w
            self.uf.merge(u,v)
        return weight