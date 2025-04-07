from bisect import bisect_left, bisect
class CompressedLazySegmentTree:
    INF = 1<<61

    class Shrink:
        def __init__(self, num):
            self.num = sorted([i for i in set(num)])
            self.shr = {v: i for i, v in enumerate(self.num)}
        
        def __len__(self):
            return len(self.num)

        def original(self, shr):
            """圧縮後の値から元の値を返す"""
            return self.num[shr]

        def shrink(self, orig):
            """元の値から圧縮後の値を返す"""
            if orig not in self.shr:
                self.shr[orig] = bisect_left(self.num, orig)
            return self.shr[orig]
        
        def __call__(self, orig):
            return self.shrink(orig)
        
    def __init__(self, op, e, mapping, composition, id, num):
        """
        op(x,y): 二項演算
        e: 単位元
        mapping(f,x): 作用 xにfを作用
        composition(g,f): 合成 g*f gが後の操作
        id: 恒等写像
        num: 直接アクセスする数字
        """
        self._shr = self.Shrink(num)
        self._n = len(self._shr)
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id
        self._log = (self._n-1).bit_length()
        self._size = 1 << self._log
        self._tree = [e for _ in range(self._size*2)]
        self._lazy = [id for _ in range(self._size*2)]
    
    def get(self, i):
        return self._get(i)
    
    def __getitem__(self, i):
        return self._get(i)
    
    def set(self, i, x):
        self._set(i, x)
    
    def __setitem__(self, i, x):
        self._set(i, x)

    def prod(self, l, r):
        """[l,r)"""
        return self._prod(l, r)
    
    def prod_left(self, r):
        """[-inf, r)"""
        return self._prod(-self.INF, r)
    
    def prod_right(self, l):
        """[l, inf)"""
        return self._prod(l, self.INF)
    
    def prod_all(self):
        return self._tree[1]
    
    def apply(self, l, r, f):
        """[l, r)にfを作用"""
        self._apply(l, r, f)
    
    def apply_left(self, r, f):
        self._apply(-self.INF, r, f)
    
    def apply_right(self, l, f):
        self._apply(l, self.INF, f)
    
    def max_right(self, l, f):
        """prod[l,j)でfuncを満たす最大のjを返す"""
        return self._max_right(l, f)
    
    def min_left(self, r, f):
        """prod[j,r)でfuncを満たす最小のjを返す"""
        return self._min_left(r, f)
    
    def __str__(self):
        idx = [self._shr.original(i) for i in range(self._n)]
        val = [self[i] for i in idx]
        return f'CompressedLazySegmentTree (\n index {idx}\n value {val}\n)'


    def _update(self, i):
        """tree[i]を更新"""
        self._tree[i] = self._op(self._tree[2*i], self._tree[2*i+1])

    def _all_apply(self, i, f):
        """tree[i],lazy[i]にfを作用"""
        self._tree[i] = self._mapping(f, self._tree[i])
        if i < self._size:
            self._lazy[i] = self._composition(f, self._lazy[i])
    
    def _push(self, i):
        """１つ下に伝播"""
        self._all_apply(2*i, self._lazy[i])
        self._all_apply(2*i+1, self._lazy[i])
        self._lazy[i] = self._id
    
    def _get(self, i):
        return self.prod(i, i+1)
    
    def _set(self, p, x):
        p = self._shr(p)
        p += self._size
        for i in range(self._log, 0, -1): #lazyを上から伝播させて
            self._push(p >> i)
        self._tree[p] = x
        while p: #普通のセグ木と同じように更新
            p >>= 1
            self._update(p)
    
    def _prod(self, l, r):
        if l == r:
            return self._e
        l = self._shr(l)
        r = self._shr(r)
        l += self._size
        r += self._size
        for i in range(self._log, 0, -1): #必要な部分のlazyを伝播
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push(r-1 >> i)
        lt = self._e
        rt = self._e
        while l < r:
            if l & 1:#右側だけなら
                lt = self._op(lt, self._tree[l])
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1:#左側だけなら
                r -= 1
                rt = self._op(self._tree[r], rt)
            l >>= 1
            r >>= 1
        return self._op(lt, rt)
    
    def _apply(self, l, r, f):
        if l == r:
            return
        l = self._shr(l)
        r = self._shr(r)
        l += self._size
        r += self._size
        for i in range(self._log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push(r-1 >> i)
        
        tmp_l = l
        tmp_r = r
        while l < r:
            if l & 1:
                self._all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._all_apply(r, f)
            l >>= 1
            r >>= 1
        
        l = tmp_l
        r = tmp_r
        for i in range(1, self._log+1):
            if ((l >> i) << i) != l:
                self._update(l >> i)
            if ((r >> i) << i) != r:
                self._update(r-1 >> i)
    
    def _max_right(self, l, f):
        l = self._shr(l)
        if l == self._n:
            return self.INF
        
        l += self._size
        #上に移動するときに見るところのlazyを伝播
        for i in range(self._log, 0, -1):
            self._push(l >> i)
        
        val = self._e
        while True:
            while not l & 1:
                l >>= 1
            if not f(self._op(val, self._tree[l])):
                while l < self._size:
                    self._push(l)#右側は伝播できてないのでする
                    l <<= 1
                    if f(self._op(val, self._tree[l])):
                        val = self._op(val, self._tree[l])
                        l += 1
                return self._shr.original(l - self._size)
            val = self._op(val, self._tree[l])
            l += 1
            if l & -l == l:
                return self.INF
    
    def _min_left(self, r, f):
        r = self._shr(r)
        if r == 0:
            return -self.INF
        
        r += self._size
        for i in range(self._log, 0, -1):
            self._push((r-1) >> i)
        
        val = self._e
        while True:
            while not r & 1:
                r >>= 1
            if not f(self._op(val, self._tree[r-1])):
                while r < self._size:
                    self._push(r-1)
                    r <<= 1
                    if f(self._op(val, self._tree[r-1])):
                        r -= 1
                        val = self._op(val, self._tree[r])
                return self._shr.original(r - self._size)
            r -= 1
            val = self._op(val, self._tree[r])
            if r & -r == r:
                return -self.INF