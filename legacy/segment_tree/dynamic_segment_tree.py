class DynamicSegmentTree:
    def __init__(self,op,e,lower,upper):
        """[lower,upper)"""
        self.op = op
        self.e = e
        self.lower = lower
        self.upper = upper
        self.size = (1 << (upper-lower).bit_length())
        self.tree = dict()
    
    def _tree(self,i):
        return self.tree[i] if i in self.tree else self.e
    
    def __getitem__(self,i):
        return self._tree(i + self.size - self.lower)
    
    def set(self,p,x):
        p += self.size - self.lower
        self.tree[p] = x
        while p:
            p >>= 1
            self.tree[p] = self.op(self._tree(2*p), self._tree(2*p+1))
        
    def prod(self,l,r):
        lt, rt = self.e, self.e
        l += self.size - self.lower
        r += self.size - self.lower
        while l < r:
            if l & 1:
                lt = self.op(lt,self._tree(l))
                l += 1
            if r & 1:
                r -= 1
                rt = self.op(self._tree(r),rt)
            l >>= 1
            r >>= 1
        return self.op(lt,rt)
    
    def max_right(self,l,f):
        """prod[l,j)でfuncを満たす最大のjを返す"""
        if l == self.upper:
            return self.upper
        
        l += self.size - self.lower
        val = self.e
        while True:
            while not l & 1:
                l >>= 1
            if not f(self.op(val,self._tree(l))):
                while l < self.size - self.lower:
                    l <<= 1
                    if f(self.op(val,self._tree(l))):
                        val = self.op(val,self._tree(l))
                        l += 1
                return l - self.size + self.lower
            val = self.op(val,self._tree(l))
            l += 1
            if l & -l == l:
                return self.upper
    
    def min_left(self,r,f):
        """prod[j,r)でfuncを満たす最小のjを返す"""
        if r == self.lower:
            return self.lower
        
        r += self.size - self.lower
        val = self.e
        while True:
            while not r & 1:
                r >>= 1
            if not f(self.op(val,self._tree(r-1))):
                while r < self.size - self.lower:
                    r <<= 1
                    if f(self.op(val,self._tree(r-1))):
                        r -= 1
                        val = self.op(val,self._tree(r))
                return r - self.size + self.lower
            r -= 1
            val = self.op(val,self._tree(r))
            if r & -r == r:
                return self.lower