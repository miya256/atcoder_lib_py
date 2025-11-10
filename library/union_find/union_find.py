class UnionFind:
    """
    連結を管理するデータ構造。計算量はアッカーマン関数の逆関数
    
    Attributes:\n
        element_list   : 初期化で生成した要素が入る
        element_dict   : addによって追加したもの
        component_count: 連結成分の個数
    
    Methods:\n
        element(id) : idをElememt型で取得
        contains(id): idが存在するか
        add(id)     : 頂点idを追加
        leader(v)   : vの属する連結成分の根
        merge(u, v) : u, vを連結
        same(u, v)  : u, vが連結か
        size(v)     : vの属する連結成分の要素数
        members(v)  : vの属する連結成分の要素
        leaders     : すべてのleaderを列挙
        groups      : すべてのleader, memberを列挙
    """

    class Element:
        """追加でデータが必要なときは、ここに直接かく"""
        def __init__(self, id: int) -> None:
            self.id = id
            self.parent = None
            self.size = 1
        
        def merge(self, other: "UnionFind.Element") -> None:
            """selfにotherをmerge"""
            other.parent = self
            self.size += other.size
        
        def should_parent(self, other: "UnionFind.Element") -> bool:
            """selfにotherをmergeするとき、こうなっていればok"""
            return self.size > other.size
        
        def __repr__(self) -> str:
            return f'{self.id}'
    
    def __init__(self, n: int = 0) -> None:
        self._n = n
        self._component_count = n
        self._element_list = [UnionFind.Element(i) for i in range(n)]
        self._element_dict = {}
    
    def _in_element_list(self, id: object) -> bool:
        """idが初期のやつか"""
        return isinstance(id, int) and id < len(self._element_list)
    
    def element(self, id: object) -> Element:
        """頂点idをElement型で取得"""
        if self._in_element_list(id):
            return self._element_list[id]
        return self._element_dict[id]
    
    def __getitem__(self, id: object) -> Element:
        """頂点idをElement型で取得"""
        return self.element(id)
    
    def contains(self, id: object) -> bool:
        """idが存在するか"""
        if self._in_element_list(id):
            return True
        return id in self._element_dict
    
    def __contains__(self, id: object) -> bool:
        """idが存在するか"""
        return self.contains(id)
    
    def add(self, id: object) -> None:
        """頂点idを追加。int型でもdictのほうに追加される"""
        assert id not in self, f'{id}はすでに存在します'
        self._element_dict[id] = UnionFind.Element(id)
        self._n += 1
        self._component_count += 1
    
    def leader(self, id: object) -> object:
        """vの属する連結成分の根"""
        v = self.element(id)
        if v.parent:
            stack = []
            while v.parent:
                stack.append(v)
                v = v.parent
            while stack:
                stack.pop().parent = v
        return v.id
    
    def merge(self, u: object, v: object) -> bool:
        """u, vを連結"""
        ru = self.element(self.leader(u))
        rv = self.element(self.leader(v))
        if ru == rv: #すでに連結なら
            return False
        self._component_count -= 1
        if not ru.should_parent(rv):
            ru, rv = rv, ru
        ru.merge(rv) #ruにrvをmerge
        return True
    
    def same(self, u: object, v: object) -> bool:
        """u, vが連結か"""
        return self.leader(u) == self.leader(v)
    
    def size(self, v: object) -> int:
        """vの連結成分の要素数"""
        return self.element(self.leader(v)).size
    
    @property
    def component_count(self) -> int:
        """連結成分の個数"""
        return self._component_count
    
    def members(self, v: object) -> list[object]:
        """vの連結成分の要素を列挙"""
        rv = self.leader(v)
        members = []
        members.extend([i for i, v in enumerate(self._element_list) if self.leader(i) ==  rv])
        members.extend([i for i, v in self._element_dict.items() if self.leader(i) == rv])
        return members
    
    @property
    def leaders(self) -> list[object]:
        """leaderを列挙"""
        leaders = []
        leaders.extend([i for i, v in enumerate(self._element_list) if v.parent is None])
        leaders.extend([i for i, v in self._element_dict.items() if v.parent is None])
        return leaders
    
    @property
    def groups(self) -> dict[object, list[object]]:
        """すべてのleaderとmembersを列挙"""
        group = {}
        for i, v in enumerate(self._element_list):
            group.setdefault(self.leader(i), []).append(i)
        for i, v in self._element_dict.items():
            group.setdefault(self.leader(i), []).append(i)
        return group
    
    def __repr__(self) -> str:
        string = ["UnionFind (\n"]
        for leader, members in self.groups.items():
            string.append(f'  leader={leader}, members={members}\n')
        string.append(")")
        return ''.join(string)