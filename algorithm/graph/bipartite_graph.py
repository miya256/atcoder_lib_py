import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class Graph:
    def __init__(self,g):
        if isinstance(g,int):
            g = [[] for _ in range(g)]
        self.n = len(g)
        self.graph = g
        self.color = [-1] * self.n

    def __getitem__(self,i):
        return self.graph[i]

    def add_edge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def dfs(self,v):
        for nv in self[v]:
            if self.color[nv] == self.color[v]:
                return False
            if self.color[nv] != -1:
                continue
            self.color[nv] = self.color[v] ^ 1
            if not self.dfs(nv):
                return False
        return True
    
    def isBipartite(self):
        for v in range(self.n):
            if self.color[v] != -1:
                continue
            self.color[v] = 0
            if not self.dfs(v):
                return False
        return True


#u-vについて、(u_a,v_b)を、(u_b,v_a)をmerge
#v_aと_v_bが同じ連結成分にあったら二部グラフでない
class UnionFind:
    class Element:
        def __init__(self,value):
            self.value = value
            self.parent = None
            self.size = 1
        
        def merge(self,other):
            other.parent = self
            self.size += other.size
            
    def __init__(self,n=0):
        self.n = 0 #頂点数
        self.cc = 0 #連結成分の個数
        self.elements = {i:self.Node(i) for i in range(n)}
    
    def add(self,value):
        """頂点を追加する"""
        assert value not in self.elements, f'{value}はすでに存在します'
        self.elements[value] = self.Element(value)
        self.n += 1
        self.cc += 1
    
    def exist(self,value):
        return value in self.elements
    
    def leader(self,v): #vはelementsのkey
        """頂点vの属する連結成分の根"""
        v = self.elements[v]
        if v.parent:
            stack = []
            while v.parent:
                stack.append(v)
                v = v.parent
            while stack:
                stack.pop().parent = v
        return v
    
    def merge(self,u,v):
        """u,vを連結"""
        ru = self.leader(u)
        rv = self.leader(v)
        if ru == rv:
            return False
        self.cc -= 1
        if ru.size < rv.size:#根をどっちにするかは、その都度考える
            ru,rv = rv,ru
        ru.merge(rv) #ruにrvをmerge
        return True
    
    def same(self,u,v):
        """u,vが連結か"""
        return self.leader(u) == self.leader(v)
    
    def size(self,v):
        """vの属する連結成分の要素数"""
        return self.leader(v).size
    
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

def isbipartite(n,edge):
    uf = UnionFind(n)
    for u,v in edge:
        uf.merge(u,2*v)
        uf.merge(2*u,v)
    for v in range(n):
        if uf.same(v,2*v):
            return False
    return True