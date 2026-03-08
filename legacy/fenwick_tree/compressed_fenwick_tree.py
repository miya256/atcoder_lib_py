from bisect import bisect_left, bisect
class CompressedFenwickTree:
    """座標圧縮を用いたFenwickTree"""
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
        
    def __init__(self, num):
        self._comp = self.Compressor(num)
        self._n = len(self._comp)
        self._tree = [0 for _ in range(self._n)]
        self._all_sum = 0
    
    def get(self, i):
        return self._sum(i, i+1)
    
    def __getitem__(self, i):
        return self.get(i)
    
    def add(self, i, x):
        """i番目にxを足す"""
        self._add(i, x)

    def set(self, i, x):
        """加えるではなく、更新"""
        self.add(i, x-self.get(i))
    
    def __setitem__(self, i, x):
        self.set(i, x)
    
    def sum(self, l, r):
        """[l,r)の和"""
        return self._sum(l, r)
    
    def sum_left(self, r):
        """[-inf, r)の和"""
        return self._sum(-self.INF, r)
    
    def sum_right(self, l):
        """[l, inf)の和"""
        return self._sum(l, self.INF)
    
    def sum_all(self):
        """すべての和"""
        return self._all_sum
    
    def bisect_left(self, x):
        """累積和がx以上になるindex"""
        return self._bisect_left(x)
    
    def bisect_right(self, x):
        """累積和がxを超えるindex"""
        return self._bisect_right(x)
    
    def __str__(self):
        idx = [self._comp.original(i) for i in range(self._n)]
        val = [self[i] for i in idx]
        return f'CompressedFenwickTree (\n index {idx}\n value {val}\n)'
    

    def _add(self, i, x):
        self._all_sum += x
        i = self._comp(i)
        i += 1
        while i <= self._n:
            self._tree[i-1] += x
            i += -i & i

    def _prefix_sum(self, i):
        sum = 0
        while i > 0:
            sum += self._tree[i-1]
            i -= -i & i
        return sum

    def _sum(self, l, r):
        """[l,r)"""
        l, r = self._comp(l), self._comp(r)
        return self._prefix_sum(r) - self._prefix_sum(l)
    
    def _bisect_left(self, x):
        i = 1 << self._n.bit_length()-1
        val = 0
        while not i & 1:
            if i-1 < self._n and val + self._tree[i-1] < x:
                val += self._tree[i-1]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return self._comp.original(i-1 + (val + self._tree[i-1] < x))
    
    def _bisect_right(self, x):
        i = 1 << self._n.bit_length()-1
        val = 0
        while not i & 1:
            if i-1 < self._n and val + self._tree[i-1] <= x:
                val += self._tree[i-1]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return self._comp.original(i-1 + (val + self._tree[i-1] <= x))