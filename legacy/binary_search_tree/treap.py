#競プロ向きではなさそう

import random
class Treap:
    class Node:
        def __init__(self,value):
            self.value = value
            self.priority = random.random()
            self.left = None
            self.right = None
            self.size = 1
        
        def _update(self):
            self.size = 1
            if self.left:
                self.size += self.left.size
            if self.right:
                self.size += self.right.size
            return self
        
        def __str__(self):
            return str(self.value)
    
    def __init__(self,root=None):
        self.root = root
    
    def __len__(self):
        return self._size(self.root)
    
    def __getitem__(self,i):
        node = self.root
        while True:
            if i < self._size(node.left):
                node = node.left
            elif i > self._size(node.left):
                i -= self._size(node.left) + 1
                node = node.right
            else:
                return node.value

    def __iter__(self):
        yield from self._dfs(self.root)
    
    def _dfs(self,node):
        if node is not None:
            yield from self._dfs(node.left)
            yield node.value
            yield from self._dfs(node.right)
    
    def _size(self,node):
        return node.size if node else 0
        
    def _merge(self,l:Node,r:Node):
        if l is None: return r
        if r is None: return l

        if l.priority > r.priority:
            l.right = self._merge(l.right, r)
            return l._update()
        else:
            r.left = self._merge(l,r.left)
            return r._update()
        
    def _split(self,node,k): #[0,k),[k,n)
        if node is None:
            return None,None
        if k <= self._size(node.left):
            l,r = self._split(node.left,k)
            node.left = r
            return l, node._update()
        else:
            l,r = self._split(node.right,k-self._size(node.left)-1)
            node.right = l
            return node._update(), r
    
    def add(self,i,value):
        l,r = self._split(self.root,i)
        self.root = self._merge(l,self.Node(value))
        self.root = self._merge(self.root,r)
    
    def pop(self,i):
        l,r = self._split(self.root,i)
        mid,r = self._split(r,1)
        self.root = self._merge(l,r)
        return mid.value
    
    def split(self,i):
        l,r = self._split(self.root,i)
        return Treap(l), Treap(r)
    
    def __str__(self):
        return f'{list(self.__iter__())}'