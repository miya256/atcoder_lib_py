from typing import Generic, TypeVar, Callable, Iterator

Monoid = TypeVar("Monoid")
Operator = TypeVar("Operator")

class LazySegmentTree(Generic[Monoid, Operator]):
    """
    区間作用、区間取得を O(log n) で計算

    Attributes:
        op(x,y)         : 二項演算
        e               : 単位元
        mapping(f,x)    : 作用 xにfを作用
        composition(g,f): 合成 g*f gが後の操作
        id              : 恒等写像

    Methods:
        get(i)        : i番目を取得
        set(i, x)     : i番目をxにする
        apply(l, r, f): 区間[l,r)にfを作用
        prod(i, x)    : 区間[l, r)の積
        all_prod()    : 全体の積    
        max_right(l, condition): condition(prod[l,j))が真になる最大のjを返す
        min_left(r, condition) : condition(prod[j,r))が真になる最小のjを返す
    """
    def __init__(
        self,
        op: Callable[[Monoid, Monoid], Monoid],
        e: Monoid,
        mapping: Callable[[Operator, Monoid], Monoid],
        composition: Callable[[Operator, Operator], Operator],
        id: Operator,
        data: list[Monoid] | int
    ) -> None:
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
    
    def _build(self, data: list[Monoid]) -> None:
        for i,val in enumerate(data):
            self._tree[i+self._size] = val
        for i in range(self._size-1, 0, -1):
            self._update(i)
    
    def __len__(self) -> int:
        return self._n

    def __getitem__(self, i: int) -> Monoid:
        return self.get(i)
    
    def __setitem__(self, i: int, x: Monoid) -> None:
        self.set(i, x)
    
    def __iter__(self) -> Iterator[Monoid]:
        for i in range(self._n):
            yield self.get(i)
    
    def __repr__(self) -> str:
        return f'LazySegmentTree {list(self)}'
    
    def get(self, p: int) -> Monoid:
        p += self._size
        for i in range(self._log, 0, -1): #lazyを上から伝播させて
            self._push(p >> i)
        return self._tree[p]
    
    def set(self, p: int, x: Monoid) -> None:
        p += self._size
        for i in range(self._log, 0, -1): #lazyを上から伝播させて
            self._push(p >> i)
        self._tree[p] = x
        while p: #普通のセグ木と同じように更新
            p >>= 1
            self._update(p)
    
    def prod(self, l: int, r: int) -> Monoid:
        """区間[l, r)の積"""
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
    
    def all_prod(self) -> Monoid:
        return self._tree[1]
    
    def apply(self, l: int, r: int, f: Operator) -> None:
        """区間[l, r)にfを作用"""
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
    
    def max_right(self, l: int, condition: Callable[[Monoid], bool]) -> int:
        """condition(prod[l,j))が真になる最大のjを返す"""
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
            if not condition(self._op(val, self._tree[l])):
                while l < self._size:
                    self._push(l)#右側は伝播できてないのでする
                    l <<= 1
                    if condition(self._op(val, self._tree[l])):
                        val = self._op(val, self._tree[l])
                        l += 1
                return l - self._size
            val = self._op(val, self._tree[l])
            l += 1
            if l & -l == l:
                return self._n
    
    def min_left(self, r: int, condition: Callable[[Monoid], bool]) -> int:
        """condition(prod[j,r))が真になる最小のjを返す"""
        if r == 0:
            return 0
        
        r += self._size
        for i in range(self._log, 0, -1):
            self._push((r-1) >> i)
        
        val = self._e
        while True:
            while not r & 1:
                r >>= 1
            if not condition(self._op(val, self._tree[r-1])):
                while r < self._size:
                    self._push(r-1)
                    r <<= 1
                    if condition(self._op(val, self._tree[r-1])):
                        r -= 1
                        val = self._op(val, self._tree[r])
                return r - self._size
            r -= 1
            val = self._op(val, self._tree[r])
            if r & -r == r:
                return 0
            
    def _update(self, i: int) -> None:
        """tree[i]を更新"""
        self._tree[i] = self._op(self._tree[2*i], self._tree[2*i+1])
    
    def _all_apply(self, i: int, f: Operator) -> None:
        """tree[i],lazy[i]にfを作用"""
        self._tree[i] = self._mapping(f, self._tree[i])
        if i < self._size:
            self._lazy[i] = self._composition(f, self._lazy[i])
    
    def _push(self, i: int) -> None:
        """１つ下に伝播"""
        self._all_apply(2*i, self._lazy[i])
        self._all_apply(2*i+1, self._lazy[i])
        self._lazy[i] = self._id