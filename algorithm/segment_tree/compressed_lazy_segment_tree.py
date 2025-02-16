from bisect import bisect_left, bisect
class CompressedLazySegmentTree:
    class Shrink:
        def __init__(self,num):
            self.num = sorted([i for i in set(num)])
            self.shr = {v:i for i,v in enumerate(self.num)}
        
        def __len__(self):
            return len(self.num)

        def original(self,shr):
            """圧縮後の値から元の値を返す"""
            return self.num[shr]

        def shrink(self,orig):
            """元の値から圧縮後の値を返す"""
            if orig not in self.shr:
                self.shr[orig] = bisect_left(self.num,orig)
            return self.shr[orig]
        
        def __call__(self,orig):
            return self.shrink(orig)
        
    def __init__(self,op,e,mapping,composition,id,num):
        """演算,単位元,作用,合成,恒等写像,list or len"""
        self.shr = self.Shrink(num)
        self.n = len(self.shr)
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id
        self.log = (self.n-1).bit_length()
        self.size = 1 << self.log
        self.tree = [e for _ in range(self.size*2)]
        self.lazy = [id for _ in range(self.size*2)]

    def _update(self,k):
        """tree[k]を更新"""
        self.tree[k] = self.op(self.tree[2*k],self.tree[2*k+1])
    
    def _all_apply(self,k,f):
        """tree[k],lazy[k]にfを作用"""
        self.tree[k] = self.mapping(f,self.tree[k])
        if k < self.size:
            self.lazy[k] = self.composition(f,self.lazy[k])
    
    def _push(self,k):
        """１つ下に伝播"""
        self._all_apply(2*k,self.lazy[k])
        self._all_apply(2*k+1,self.lazy[k])
        self.lazy[k] = self.id
    
    def __getitem__(self,p):
        return self.prod(p,p+1)
    
    def set(self,p,x):
        p = self.shr(p)
        p += self.size
        for i in range(self.log,0,-1): #lazyを上から伝播させて
            self._push(p >> i)
        self.tree[p] = x
        while p: #普通のセグ木と同じように更新
            p >>= 1
            self._update(p)
    
    def prod(self,l,r):
        if l == r:
            return self.e
        l,r = self.shr(l),self.shr(r)
        l += self.size
        r += self.size
        for i in range(self.log,0,-1): #必要な部分のlazyを伝播
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push(r-1 >> i)
        lt = self.e
        rt = self.e
        while l < r:
            if l & 1:#右側だけなら
                lt = self.op(lt,self.tree[l])
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1:#左側だけなら
                r -= 1
                rt = self.op(self.tree[r],rt)
            l >>= 1
            r >>= 1
        return self.op(lt,rt)
    
    def all_prod(self):
        return self.tree[1]
    
    def apply(self,l,r,f):
        if l == r:
            return
        l,r = self.shr(l),self.shr(r)
        l += self.size
        r += self.size
        for i in range(self.log,0,-1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push(r-1 >> i)
        
        tmp_l = l
        tmp_r = r
        while l < r:
            if l & 1:
                self._all_apply(l,f)
                l += 1
            if r & 1:
                r -= 1
                self._all_apply(r,f)
            l >>= 1
            r >>= 1
        
        l = tmp_l
        r = tmp_r
        for i in range(1,self.log+1):
            if ((l >> i) << i) != l:
                self._update(l >> i)
            if ((r >> i) << i) != r:
                self._update(r-1 >> i)
    
    def max_right(self,l,f):
        l = self.shr(l)
        if l == self.n:
            return self.shr.original(self.n-1)
        
        l += self.size
        #上に移動するときに見るところのlazyを伝播
        for i in range(self.log,0,-1):
            self._push(l >> i)
        
        val = self.e
        while True:
            while not l & 1:
                l >>= 1
            if not f(self.op(val,self.tree[l])):
                while l < self.size:
                    self._push(l)#右側は伝播できてないのでする
                    l <<= 1
                    if f(self.op(val,self.tree[l])):
                        val = self.op(val,self.tree[l])
                        l += 1
                return self.shr.original(l - self.size)
            val = self.op(val,self.tree[l])
            l += 1
            if l & -l == l:
                return self.shr.original(self.n-1)
    
    def min_left(self,r,f):
        r = self.shr(r)
        if r == 0:
            return self.shr.original(0)
        
        r += self.size
        for i in range(self.log,0,-1):
            self._push((r-1) >> i)
        
        val = self.e
        while True:
            while not r & 1:
                r >>= 1
            if not f(self.op(val,self.tree[r-1])):
                while r < self.size:
                    self._push(r-1)
                    r <<= 1
                    if f(self.op(val,self.tree[r-1])):
                        r -= 1
                        val = self.op(val,self.tree[r])
                return self.shr.original(r - self.size)
            r -= 1
            val = self.op(val,self.tree[r])
            if r & -r == r:
                return self.shr.original(0)
    
    def __str__(self):
        return f'LazySegmentTree {[self[self.shr.original(i)] for i in range(self.n)]}'
