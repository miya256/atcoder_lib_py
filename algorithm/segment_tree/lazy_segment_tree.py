#1点取得なら、BITやセグ木でいいか確認。
#実際にBITのほうが速い

#Range Affine Range Sum の場合、
#ちゃんと区間の長さ分の定数を足さないとだめ
class LazySegmentTree:
    def __init__(self, op, e, mapping, composition, id, data):
        """
        op(x,y): 二項演算
        e: 単位元
        mapping(f,x): 作用 xにfを作用
        composition(g,f): 合成 g*f gが後の操作
        id: 恒等写像
        data: list or len
        """
        if isinstance(data, int):
            data = [e for _ in range(data)]
        self._n = len(data)
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id
        self._log = (len(data)-1).bit_length()
        self._size = 1 << self._log
        self._tree = [e for _ in range(self._size*2)]
        self._lazy = [id for _ in range(self._size*2)]
        self._build(data)
    
    def _build(self, data):
        for i,val in enumerate(data):
            self._tree[i+self._size] = val
        for i in range(self._size-1, 0, -1):
            self._update(i)
    
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
    
    def all_prod(self):
        return self._tree[1]
    
    def apply(self, l, r, f):
        """[l, r)にfを作用"""
        self._apply(l, r, f)
    
    def max_right(self, l, f):
        """prod[l,j)でfuncを満たす最大のjを返す"""
        return self._max_right(l, f)
    
    def min_left(self, r, f):
        """prod[j,r)でfuncを満たす最小のjを返す"""
        return self._min_left(r, f)
    
    def __str__(self):
        return f'LazySegmentTree {[self[i] for i in range(self._n)]}'
    

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
    
    def _get(self, p):
        p += self._size
        for i in range(self._log, 0, -1): #lazyを上から伝播させて
            self._push(p >> i)
        return self._tree[p]
    
    def _set(self, p, x):
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
        if l == self._n:
            return self._n
        
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
                return l - self._size
            val = self._op(val, self._tree[l])
            l += 1
            if l & -l == l:
                return self._n
    
    def _min_left(self, r, f):
        if r == 0:
            return 0
        
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
                return r - self._size
            r -= 1
            val = self._op(val, self._tree[r])
            if r & -r == r:
                return 0