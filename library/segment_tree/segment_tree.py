#データクラスをうまく持てないか検討中
#やっぱ型はほとんどeと同じ型だし、
# 遅延セグ木だと、データと作用素で型違うから、objectはちょっとやだ

class SegmentTree:
    """
    一点更新、区間取得を O(log n) で計算

    Attributes\n:
        op(x, y): xとyの二項演算（関数型）
        e       : opの単位元

    Methods:\n
        get(i)    : i番目を取得
        set(i, x) : i番目をxにする
        prod(i, x): 区間[l, r)の積
        all_prod(): 全体の積    
        max_right(l, condition): condition(prod[l,j))が真になる最大のjを返す
        min_left(r, condition) : condition(prod[j,r))が真になる最小のjを返す
    """
    
    def __init__(self, op: object, e: object, data: list[object]|int) -> None:
        if isinstance(data, int):
            data = [e for _ in range(data)]
        self._n = len(data)
        self._op = op
        self._e = e
        self._size = 1 << (len(data)-1).bit_length() #最下段の長さ
        self._tree = [e for _ in range(self._size*2)] #tree[1]が最上段,tree[size]が元のdata[0]
        self._build(data)
    
    def _build(self, data: list[object]) -> None:
        for i, val in enumerate(data):
            self._tree[i+self._size] = val
        for i in range(self._size-1, 0, -1):
            self._update(i)
    
    def _update(self, i: int) -> None:
        self._tree[i] = self._op(self._tree[2*i], self._tree[2*i+1])
    
    def get(self, i: int) -> object:
        """i番目を取得"""
        return self._tree[i+self._size]
    
    def __getitem__(self, i: int) -> object:
        """i番目を取得"""
        return self.get(i)
    
    def set(self, i: int, x: object) -> None:
        """i番目にxを代入"""
        i += self._size
        self._tree[i] = x
        while i:
            i >>= 1
            self._update(i)
    
    def __setitem__(self, i: int, x: object) -> None:
        """i番目にxを代入"""
        self.set(i, x)
    
    def prod(self, l: int, r: int) -> object:
        """区間[l, r)の積"""
        lt, rt = self._e, self._e
        l += self._size
        r += self._size
        while l < r:
            if l & 1: #右側だけなら
                lt = self._op(lt, self._tree[l])
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1: #左側だけなら
                r -= 1
                rt = self._op(self._tree[r], rt)
            l >>= 1
            r >>= 1
        return self._op(lt, rt)
    
    def all_prod(self) -> object:
        """全体の積"""
        return self._tree[1]
    
    def max_right(self, l: int, condition: object) -> int:
        """condition(prod[l,j))が真になる最大のjを返す"""
        if l == self._n:
            return self._n
        
        l += self._size
        val = self._e #確定した区間の積
        while True:
            while not l & 1: #右ノードになるまで親に移動
                l >>= 1
            if not condition(self._op(val, self._tree[l])):
                while l < self._size: #下まで
                    l <<= 1 #左の子に移動
                    if condition(self._op(val, self._tree[l])): #満たすなら
                        val = self._op(val, self._tree[l]) #左は確定して
                        l += 1 #同じ段の右ノードに移動
                return l - self._size
            val = self._op(val, self._tree[l]) #満たすなら確定する
            l += 1 #右に移動
            if l & -l == l: #condition(prod(l,n)) = Trueなら(lが2の累乗)
                return self._n #一番右を返す
        
    def min_left(self, r: int, condition: object) -> int:
        """condition(prod[j,r))が真になる最小のjを返す"""
        if r == 0:
            return 0
        
        r += self._size
        val = self._e
        while True:
            while not r & 1:
                r >>= 1
            if not condition(self._op(val, self._tree[r-1])):
                while r < self._size:
                    r <<= 1
                    if condition(self._op(val, self._tree[r-1])):
                        r -= 1
                        val = self._op(val, self._tree[r])
                return r - self._size
            r -= 1
            val = self._op(val, self._tree[r])
            if r & -r == r:
                return 0
    
    def __repr__(self) -> str:
        return f'SegmentTree {self._tree[self._size:self._size+self._n]}'