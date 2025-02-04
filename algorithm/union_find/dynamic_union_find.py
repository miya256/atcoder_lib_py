class Node:
    def __init__(self,val):
        self.val = val
        self.parent = None
        self.size = 1
    
    def __lt__(self, other):
        return self.size < other.size
    
    def __gt__(self, other):
        return self.size > other.size
    
    def __str__(self):
        return str(self.val)

class DynamicUnionFind:
    def __init__(self):
        self.nodes = {}
    
    def leader(self, v:int):
        """頂点vの属する連結成分の根"""
        if v not in self.nodes:
            self.nodes[v] = Node(v)
        node = self.nodes[v]
        if node.parent is not None:
            stack = []
            while node.parent is not None:
                stack.append(node)
                node = node.parent
            while stack:
                stack.pop().parent = node
        return node
    
    def merge(self,u,v):
        """連結した後の根を返す"""
        ru = self.leader(u)
        rv = self.leader(v)
        if ru == rv:
            return False
        if ru < rv:#根をどっちにするかは、その都度考える
            ru,rv = rv,ru
        #ruにrvをmerge
        rv.parent = ru
        ru.size += rv.size
        return True
    
    def same(self,u,v):
        return self.leader(u) == self.leader(v)
    
    def size(self,v):
        return self.leader(v).size
    
    def roots(self):
        return [node for node in self.nodes.values() if node.parent is None]
    
    def members(self,v):
        rv = self.leader(v)
        return [v for v in self.nodes.keys() if self.leader(v) == rv]
    
    def groups(self):
        res = {i.val:list() for i in self.roots()}
        for k,v in self.nodes.items():
            res[self.leader(k).val].append(k)
        return res
    
    def count_connected_components(self):
        return len(self.roots())
    
    def __str__(self):
        return f'{self.groups()}'