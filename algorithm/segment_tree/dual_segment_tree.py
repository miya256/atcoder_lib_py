class DualSegmentTree:
    def __init__(self,op,e,data):
        """作用, 単位元, list or len"""
        if isinstance(data,int):
            data = [e for _ in range(data)]
        self.n = len(data)
        self.op = op
        self.e = e
        self.size = 1 << (len(data)-1).bit_length()#最下段の長さ
        self.tree = [e for _ in range(self.size*2)]#tree[size]が元のdata[0]
        self._build(data)
    
    def _build(self,data):
        for i,val in enumerate(data):
            self.tree[i+self.size] = val
    
    def __getitem__(self,i):
        i += self.size
        res = self.e
        while i:
            res = self.op(res,self.tree[i])
            i >>= 1
        return res
    
    def apply(self,l,r,f):
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                self.tree[l] = self.op(self.tree[l],f)
                l += 1
            if r & 1:
                r -= 1
                self.tree[r] = self.op(self.tree[r],f)
            l >>= 1
            r >>= 1
    
    def __str__(self):
        return f'DualSegmentTree {[self[i] for i in range(self.n)]}'