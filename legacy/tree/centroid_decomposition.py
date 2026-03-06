#重心分解によってつくられる木の高さはlogN
#したがって各木における重心からの何かを求めるのはNlogN
class CentroidDecomposition:
    def __init__(self,n):
        self.n = n
        self.tree = [[] for _ in range(n)]
        self.order = [-1]*n
        self.depth = [-1]*n #重心分解によってつくられる木における、重心vの深さ
        self.belong = [-1]*n #重心分解によってつくられる木における、重心vの親の木の重心
    
    def add_edge(self,u,v):
        self.tree[u].append(v)
        self.tree[v].append(u)
    
    def _dfs(self,root):
        """部分木のサイズを求める"""
        size = [1]*self.n
        stack = [(root,-1)]
        while stack:
            v,par = stack.pop()
            if v < 0: #返ってきたら
                size[par] += size[~v]
                continue
            for nv in self.tree[v]:
                if nv != par:
                    stack.append((~nv,v))
                    stack.append((nv,v))
        return size
    
    def _decomposit(self,size):
        stack = [(0,-1,0)]
        for i in range(self.n):
            v,par,d = stack.pop()
            while True: #重心までいく
                for nv in self.tree[v]:
                    if self.order[nv] == -1 and size[nv] * 2 > size[v]:
                        size[v],size[nv],v = size[v]-size[nv],size[v],nv
                        break
                else: #すべての子のサイズがn//2以下だったら
                    break
            self.order[v] = i
            self.depth[v] = d
            self.belong[v] = par
            if size[v] > 1:
                for nv in self.tree[v]:
                    if self.order[nv] == -1:
                        stack.append((nv,v,d+1))
    
    def build(self):
        size = self._dfs(0)
        self._decomposit(size)
    
    def find(self,u,v):
        """u,vをどちらも含む最も小さい部分木の重心"""
        if self.depth[u] < self.depth[v]:
            u,v = v,u
        for _ in range(self.depth[u]-self.depth[v]):
            u = self.belong[u]
        while u != v:
            u,v = self.belong[u],self.belong[v]
        return u
    
    def get(self,v):
        """vが属する木を列挙"""
        res = []
        for _ in range(self.depth[v]+1):
            res.append(v)
            v = self.belong[v]
        return res