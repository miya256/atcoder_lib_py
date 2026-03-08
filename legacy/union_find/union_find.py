#elementsは計算量やばかったら配列にする
class UnionFind:
    class Element:
        def __init__(self, id):
            self.id = id
            self.parent = None
            self.size = 1
        
        def merge(self, other):
            """selfにotherをmerge"""
            other.parent = self
            self.size += other.size
        
        def compare(self, other):
            """selfにotherをmergeするとき、こうなっていればokというのを返す"""
            return self.size > other.size
        
        def __str__(self):
            return f'{self.id}'
            
    def __init__(self, n=0):
        self._n = n #頂点数
        self._component_count = n #連結成分の個数
        self._elements = {i: UnionFind.Element(i) for i in range(n)}
    
    def element(self, id) -> Element:
        """頂点idをElement型で取得"""
        return self._elements[id]
    
    def __getitem__(self, id):
        return self.element(id)
    
    def add(self, id):
        """頂点を追加する"""
        self._add(id)
    
    def contains(self, id):
        """点idが存在するか"""
        return self._contains(id)
    
    def __contains__(self, id):
        """in演算子で呼べる"""
        return self._contains(id)
    
    def leader(self, v):
        """頂点vの属する連結成分の根"""
        return self._leader(self._elements[v]).id
    
    def merge(self, u, v):
        """u, vを連結"""
        return self._merge(self._elements[u], self._elements[v])
    
    def same(self, u, v):
        """u,vが連結か"""
        return self._same(self._elements[u], self._elements[v])
    
    def size(self, v):
        """vの属する連結成分の要素数"""
        return self._size(self._elements[v])
    
    def roots(self):
        """根を列挙"""
        return self._roots()
    
    def members(self, v):
        """vの属する連結成分の要素"""
        return self._members(self._elements[v])
    
    def groups(self):
        """根と連結成分の要素を全列挙"""
        return self._groups()
    
    def count_components(self):
        """連結成分の個数"""
        return self._component_count
    
    def __str__(self):
        return f'{self.groups()}'
    

    def _add(self, id):
        assert id not in self._elements, f'{id}はすでに存在します'
        self._elements[id] = UnionFind.Element(id)
        self._n += 1
        self._component_count += 1
    
    def _contains(self, id):
        return id in self._elements
    
    def _leader(self, v: Element) -> Element:
        if v.parent:
            stack = []
            while v.parent:
                stack.append(v)
                v = v.parent
            while stack:
                stack.pop().parent = v
        return v
    
    def _merge(self, u: Element, v: Element):
        ru = self._leader(u)
        rv = self._leader(v)
        if ru == rv:
            return False
        self._component_count -= 1
        if not ru.compare(rv):
            ru, rv = rv, ru
        ru.merge(rv) #ruにrvをmerge
        return True
    
    def _same(self, u: Element, v: Element):
        return self._leader(u) == self._leader(v)
    
    def _size(self, v: Element):
        return self._leader(v).size
    
    def _roots(self):
        return [i for i, v in self._elements.items() if v.parent is None]
    
    def _members(self, v: Element):
        rv = self._leader(v)
        return [i for i, v in self._elements.items() if self._leader(v) == rv]
    
    def _groups(self):
        group = {}
        for i, v in self._elements.items():
            group.setdefault(self._leader(v).id, []).append(i)
        return group