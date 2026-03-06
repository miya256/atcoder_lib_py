from bisect import bisect_left, bisect
class CompressedSegmentTree:
    """座標圧縮を用いたSegmentTree"""
    INF = 1<<61
    
    class Compressor:
        def __init__(self, num):
            self.num = sorted([i for i in set(num)])
            self.compressed = {v:i for i,v in enumerate(self.num)}
        
        def __len__(self):
            return len(self.num)

        def original(self, comp):
            """圧縮後の値から元の値を返す"""
            return self.num[comp]

        def compress(self, orig):
            """元の値から圧縮後の値を返す"""
            if orig not in self.compressed:
                self.compressed[orig] = bisect_left(self.num, orig)
            return self.compressed[orig]
        
        def __call__(self, orig):
            return self.compress(orig)
        
    def __init__(self, op, e, num):
        """演算, 単位元, list or len"""
        self._comp = self.Compressor(num)
        self._n = len(self._comp)
        self._op = op
        self._e = e
        self._size = 1 << (self._n-1).bit_length() #最下段の長さ
        self._tree = [e for _ in range(self._size*2)] #tree[1]が最上段,tree[size]が元のdata[0]
    
    def get(self, i):
        return self._prod(i, i+1)
    
    def __getitem__(self,i):
        return self.get(i)
    
    def set(self, i, x):
        """i番目にxを代入"""
        self._set(i, x)
    
    def __setitem__(self, i, x):
        self.set(i, x)
    
    def prod(self, l, r):
        """[l, r)"""
        return self._prod(l, r)
    
    def prod_left(self, r):
        """[-inf, r)"""
        return self._prod(-self.INF, r)
    
    def prod_right(self, l):
        """[l, inf)"""
        return self._prod(l, self.INF)
    
    def prod_all(self):
        return self._tree[1]
    
    def max_right(self, l, f):
        """prod[l,j)でfuncを満たす最大のjを返す"""
        return self._max_right(l, f)
    
    def min_left(self, r, f):
        """prod[j,r)でfuncを満たす最小のjを返す"""
        return self._min_left(r, f)
    
    def __str__(self):
        idx = [self._comp.original(i) for i in range(self._n)]
        val = [self[i] for i in idx]
        return f'CompressedSegmentTree (\n index {idx}\n value {val}\n)'


    def _update(self, i):
        self._tree[i] = self._op(self._tree[2*i], self._tree[2*i+1])
    
    def _set(self, i, x):
        i = self._comp(i)
        i += self._size
        self._tree[i] = x
        while i:
            i >>= 1
            self._update(i)
    
    def _prod(self, l, r):
        lt, rt = self._e, self._e
        l, r = self._comp(l), self._comp(r)
        l += self._size
        r += self._size
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
    
    def _max_right(self, l, f):
        l = self._comp(l)
        if l == self._n:
            return self._comp.original(self._n-1)
        
        l += self._size
        val = self._e#確定した区間の積
        while True:
            while not l & 1: #右ノードになるまで親に移動
                l >>= 1
            if not f(self._op(val, self._tree[l])):
                while l < self._size: #下まで
                    l <<= 1 #左の子に移動
                    if f(self._op(val, self._tree[l])): #満たすなら
                        val = self._op(val, self._tree[l]) #左は確定して
                        l += 1 #同じ段の右ノードに移動
                return self._comp.original(l - self._size)
            val = self._op(val, self._tree[l]) #満たすなら確定する
            l += 1#右に移動
            if l & -l == l: #f(prod(l,n)) = Trueなら(lが2の累乗)
                return self.INF #dataの一番右を返す
    
    def _min_left(self, r, f):
        r = self._comp(r)
        if r == 0:
            return -self.INF
        
        r += self._size
        val = self._e
        while True:
            while not r & 1:
                r >>= 1
            if not f(self._op(val, self._tree[r-1])):
                while r < self._size:
                    r <<= 1
                    if f(self._op(val, self._tree[r-1])):
                        r -= 1
                        val = self._op(val, self._tree[r])
                return self._comp.original(r - self._size)
            r -= 1
            val = self._op(val, self._tree[r])
            if r & -r == r: #f(prod(0,r)) = Trueなら(rが2の累乗)
                return -self.INF