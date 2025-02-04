class WeightedUnionFind:
    def __init__(self,n):
        self.n = n
        self.parent = [i for i in range(n)]
        self.size = [1]*n
        self.weight = [None]*n #頂点vの重み
        self.diff = [0]*n #親との差(weight[v] - weight[par[v]])
    
    def leader(self,v):
        if v != self.parent[v]:
            stack = []
            while v != self.parent[v]:
                stack.append(v)
                v = self.parent[v]
            while stack:
                u = stack.pop()
                self.diff[u] += self.diff[self.parent[u]]
                self.parent[u] = v
        return v
    
    def set_weight(self,v,w):
        """頂点vの重みをwと決める"""
        rv = self.leader(v)
        #weight[rv] is not None and weight[rv] != w-diff[v]
        #ならば矛盾する
        #連結成分ごと移動するとかならそのまま処理すればよい
        self.weight[rv] = w - self.diff[v]
    
    def merge(self,u,v,w):
        """w = weight[v] - weight[u]"""
        ru = self.leader(u)
        rv = self.leader(v)
        w += self.diff[u] - self.diff[v]
        if ru == rv:
            return False
        if self.size[ru] < self.size[rv]:
            ru,rv = rv,ru
            w = -w
        #ruにrvをmerge
        self.parent[rv] = ru
        self.size[ru] += self.size[rv]
        self.diff[rv] = w
        if self.weight[rv] is not None:
            self.weight[ru] = self.weight[rv] - w
        return True
    
    def same(self,u,v):
        return self.leader(u) == self.leader(v)
    
    def get_diff(self,u,v):
        """
        重みの差(weight[v]-weight[u])を返す
        連結でなくとも、双方の重みが分かれば返す
        """
        ru = self.leader(u)
        rv = self.leader(v)
        assert ru == rv or self.weight[ru] and self.weight[rv],"not connected and not decided weight"

        if ru == rv:
            return self.diff[v] - self.diff[u]
        return (self.weight[rv] + self.diff[v]) - (self.weight[ru] + self.diff[u])
    
    def get_size(self,v):
        return self.size[self.leader(v)]
    
    def get_weight(self,v):
        """重みが決まってなければ、根との差を返す"""
        rv = self.leader(v)
        if self.weight[rv] is None:
            return self.diff[v]
        return self.weight[rv] + self.diff[v]
    
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