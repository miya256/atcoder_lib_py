class LazySegmentTree:
    def __init__(self,op,e,mapping,composition,id,data):
        """演算,単位元,作用,合成,恒等写像,list or len"""
        if isinstance(data,int):
            data = [e for _ in range(data)]
        self.n = len(data)
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id
        self.log = (len(data)-1).bit_length()
        self.size = 1 << self.log
        self.tree = [e for _ in range(self.size*2)]
        self.lazy = [id for _ in range(self.size*2)]
        self._build(data)
    
    def _build(self,data):
        for i,val in enumerate(data):
            self.tree[i+self.size] = val
        for i in range(self.size-1,0,-1):
            self.tree[i] = self.op(self.tree[2*i], self.tree[2*i+1])
    
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
        p += self.size
        for i in range(self.log,0,-1): #lazyを上から伝播させて
            self._push(p >> i)
        return self.tree[p]
    
    def set(self,p,x):
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
    
    def apply(self,l,r,f):
        if l == r:
            return
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
        if l == self.n:
            return self.n
        
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
                return l - self.size
            val = self.op(val,self.tree[l])
            l += 1
            if l & -l == l:
                return self.n
    
    def min_left(self,r,f):
        if r == 0:
            return 0
        
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
                return r - self.size
            r -= 1
            val = self.op(val,self.tree[r])
            if r & -r == r:
                return 0
    
    def __str__(self):
        return f'LazySegmentTree {[self[i] for i in range(self.n)]}'


class RARS:
    """ACLのやつ"""
    mod = 998244353
    e = (0,0)
    id_ = (1,0)

    def op(x,y):
        return (x[0]+y[0]) % RARS.mod
    
    def mapping(f,x):
        return (f[0]*x[0] + f[1]*x[1]) % RARS.mod, x[1]
    
    def composition(g,f):
        return (f[0]*g[0]) % RARS.mod, (f[1]*g[0]+g[1]) % RARS.mod