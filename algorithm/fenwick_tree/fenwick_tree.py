class FenwickTree:
    def __init__(self, data):
        """data: list or len"""
        if isinstance(data, int):
            data = [0 for _ in range(data)]
        self._n = len(data)
        self._data = data
        self._tree = [0] * self._n
        self._all_sum = self._build(data)
    
    def _build(self, data):
        acc = [0] * (self._n+1)
        for i in range(1, self._n+1):
            acc[i] = acc[i-1] + data[i-1]
            self._tree[i-1] = acc[i] - acc[i-(-i&i)]
        return acc[-1]
    
    def __len__(self):
        return self._n
    
    def get(self, i):
        return self._data[i]
    
    def __getitem__(self, i):
        return self.get(i)
    
    def add(self, i ,x):
        """i番目にxを足す"""
        self._add(i, x)
    
    def set(self, i, x):
        """加えるではなく、更新"""
        self._add(i, x-self._data[i])
    
    def __setitem__(self, i, x):
        self.set(i, x)

    def sum(self, l, r):
        """[l,r)の和"""
        return self._sum(l, r)
    
    def all_sum(self):
        return self._all_sum
    
    def bisect_left(self, x):
        """累積和がx以上になるindex"""
        return self._bisect_left(x)
    
    def bisect_right(self, x):
        """累積和がxを超えるindex"""
        return self._bisect_right(x)
    
    def __str__(self):
        return f'FenwickTree {self._data}'
    
    def _add(self, i, x):
        self._data[i] += x
        self._all_sum += x
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
        return i-1 + (val + self._tree[i-1] < x)
    
    def _bisect_right(self, x):
        i = 1 << self._n.bit_length()-1
        val = 0
        while not i & 1:
            if i-1 < self._n and val + self._tree[i-1] <= x:
                val += self._tree[i-1]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (val + self._tree[i-1] <= x)