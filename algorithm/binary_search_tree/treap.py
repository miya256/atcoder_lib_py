import random
class Treap:
    def __init__(self,value=None):
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
    
    @staticmethod
    def merge(l,r):
        if l is None: return r
        if r is None: return l
        if l.priority < r.priority:
            l, r = r, l
        l.right = Treap.merge(l.right, r)
        l._update()
        return l
    
    def split(self,k): #[0,k),[k,n)
        if k <= self.left.size:
            l,r = self.left.split(k)
            self.left = r
            return l, self._update()
        else:
            l,r = self.right.split(k-self.left.size-1)
            self.right = l
            return self._update(), r