class FenwickTree:
    def __init__(self, op, op_inv, e, data):
        """二項演算、逆演算、単位元、list or len"""
        if isinstance(data,int):
            data = [e for _ in range(data)]
        self._n = len(data)
        self._op = op
        self._op_inv = op_inv
        self._e = e
        self._data = data
        self._tree = [0] * self._n
        self._all_prod = self._build(data)

    def _build(self, data):
        acc = [self._e for _ in range(self._n+1)]
        for i in range(1, self._n+1):
            acc[i] = self._op(acc[i-1], data[i-1])
            self._tree[i-1] = self._op_inv(acc[i], acc[i-(-i&i)])
        return acc[-1]
    
    def __len__(self):
        return self._n
    
    def get(self, i):
        return self._data[i]
    
    def __getitem__(self, i):
        return self.get(i)
    
    def apply(self, i ,x):
        """i番目にxを作用。写像はop"""
        self._apply(i, x)
    
    def set(self, i, x):
        """加えるではなく、更新"""
        self._apply(i, self._op_inv(x, self._data[i]))
    
    def __setitem__(self, i, x):
        self.set(i, x)
    
    def prod(self, l, r):
        """[l,r)の総積"""
        return self._prod(l, r)
    
    def all_prod(self):
        return self._all_prod
    
    def __str__(self):
        return f'FenwickTree {self._data}'
    
    def _apply(self, i, x):
        self._data[i] = self._op(self._data[i], x)
        self._all_prod = self._op(self._all_prod, x)
        i += 1
        while i <= self._n:
            self._tree[i-1] = self._op(self._tree[i-1], x)
            i += -i & i

    def _prefix_prod(self, i):
        prod = self._e
        while i > 0:
            prod = self._op(prod, self._tree[i-1])
            i -= -i & i
        return prod

    def _prod(self, l, r):
        return self._op_inv(self._prefix_prod(r), self._prefix_prod(l))