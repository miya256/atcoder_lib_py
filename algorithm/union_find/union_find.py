class UnionFind:
    def __init__(self,n):
        """
        n: 頂点数
        _parent: 親
        _size: 頂点iが属する連結成分の頂点数
        """
        self.n = n
        self._parent = [i for i in range(n)]
        self._size = [1]*n #頂点の個数だけでなく、いろいろなパラメータを持たせられる
    
    def leader(self,v):
        """頂点vの属する連結成分の根"""
        if v != self._parent[v]:
            stack = []
            while v != self._parent[v]:
                stack.append(v)
                v = self._parent[v]
            while stack:
                self._parent[stack.pop()] = v
        return v
    
    def merge(self,u,v):
        """連結した後の根を返す"""
        ru = self.leader(u)
        rv = self.leader(v)
        if ru == rv:
            return False
        if self._size[ru] < self._size[rv]:#根をどっちにするかは、その都度考える
            ru,rv = rv,ru
        #ruにrvをmerge
        self._parent[rv] = ru
        self._size[ru] += self._size[rv]
        return True
    
    def same(self,u,v):
        return self.leader(u) == self.leader(v)
    
    def size(self,v):
        return self._size[self.leader(v)]
    
    def roots(self):
        return [i for i,v in enumerate(self._parent) if i == v]
    
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