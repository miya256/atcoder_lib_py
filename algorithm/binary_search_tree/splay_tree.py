class SplayTree:
    class Node:
        def __init__(self,value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None
        self.d = 0
    
    def __iter__(self):
        yield from self._dfs(self.root,0)

    def _dfs(self,node,d):
        if node is not None:
            yield from self._dfs(node.left,d+1)
            self.d = max(self.d,d)
            yield node.value
            yield from self._dfs(node.right,d+1)

    def _rotate_left(self,node):
        pivot = node.right
        node.right = pivot.left
        pivot.left = node
        return pivot
    
    def _rotate_right(self,node):
        pivot = node.left
        node.left = pivot.right
        pivot.right = node
        return pivot
    
    def splay(self,node,value): #nodeの位置にvalueの入ったノードを持ってくる
        if node is None or node.value == value:
            return node
        if value < node.value:
            if node.left is None:
                return node
            node.left = self.splay(node.left,value)
            node = self._rotate_right(node)
        else:
            if node.right is None:
                return node
            node.right = self.splay(node.right,value)
            node = self._rotate_left(node)
        return node
    
    def _add(self,node,value):
        if node is None:
            node = self.Node(value)
            return node
        if value < node.value:
            node.left = self._add(node.left,value)
        else:
            node.right = self._add(node.right,value)
        return node
    
    def add(self,value):
        self.root = self.splay(self.root,value)
        self.root = self._add(self.root,value)