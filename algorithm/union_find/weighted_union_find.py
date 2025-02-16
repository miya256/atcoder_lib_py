class WeightedUnionFind:
    class Element:
        def __init__(self,value,weight=None):
            self.value = value
            self.parent = None
            self.size = 1
            self.weight = weight
            self.diff = 0 #親との差(weight - parent.weight)
        
        def merge(self,other,w):
            other.parent = self
            self.size += other.size
            other.diff = w
            if other.weight is not None:
                self.weight = other.weight - w

    def __init__(self,n=0):
        self.n = n
        self.cc = n #連結成分の個数
        self.elements = {i:self.Element(i) for i in range(n)}
    
    def add(self,value,weight=None):
        """頂点を追加する"""
        assert value not in self.elements, f'{value}はすでに存在します'
        self.elements[value] = self.Element(value,weight)
        self.n += 1
        self.cc += 1

    def leader(self,v):
        """頂点vの属する連結成分の根"""
        v = self.elements[v]
        if v.parent:
            stack = []
            while v.parent:
                stack.append(v)
                v = v.parent
            while stack:
                u = stack.pop()
                u.diff += u.parent.diff
                u.parent = v
        return v
    
    def set_weight(self,v,w):
        """頂点vの重みをwと決める"""
        rv = self.leader(v)
        v = self.elements[v]
        #if rv.weight is not None and rv.weight != w-v.diff:
        #ならば矛盾する
        #連結成分ごと移動するとかならそのまま処理すればよい
        rv.weight = w - v.diff
    
    def merge(self,u,v,w):
        """w = v.weight - u.weight"""
        ru,rv = self.leader(u),self.leader(v)
        u,v = self.elements[u],self.elements[v]
        w += u.diff - v.diff
        if ru == rv:
            return False
        self.cc -= 1
        if ru.size < rv.size:
            ru,rv = rv,ru
            w = -w
        ru.merge(rv,w) #ruにrvをmerge
        return True
    
    def same(self,u,v):
        return self.leader(u) == self.leader(v)
    
    def diff(self,u,v):
        """
        重みの差(weight[v]-weight[u])を返す
        連結でなくとも、双方の重みが分かれば返す
        """
        ru,rv = self.leader(u),self.leader(v)
        u,v = self.elements[u],self.elements[v]
        assert ru == rv or ru.weight and rv.weight,"not connected and not decided weight"

        if ru == rv:
            return v.diff - u.diff
        return (rv.weight + v.diff) - (ru.weight + u.diff)
    
    def size(self,v):
        return self.leader(v).size
    
    def get_weight(self,v):
        """重みが決まってなければ、根との差を返す"""
        rv = self.leader(v)
        v = self.elements[v]
        if rv.weight is None:
            return v.diff
        return rv.weight + v.diff
    
    def roots(self):
        """根を列挙"""#必要に応じて、Element型のほうを返すようにする
        return [i for i,v in self.elements.items() if v.parent is None]
    
    def members(self,v):
        """vの属する連結成分の要素"""
        rv = self.leader(v)
        return [i for i,v in self.elements.items() if self.leader(i) == rv]
    
    def groups(self):
        """根と連結成分の要素を全列挙"""
        group = {i:list() for i in self.roots()}
        for i in self.elements.keys():
            group[self.leader(i)].append(i)
        return group
    
    def get_cc(self):
        """連結成分の個数"""
        return self.cc
    
    def __str__(self):
        return f'{self.groups()}'