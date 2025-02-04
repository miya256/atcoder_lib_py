class DynamicFenwickTree:
    def __init__(self,lower,upper):
        self.n = upper - lower
        self.lower = lower
        self.upper = upper
        self.data = dict()
    
    def __getitem__(self,i):
        return self.prod(i,i+1)
    
    def _data(self,i):
        return self.data[i] if i in self.data else 0
    
    def add(self, i, x):
        i -= self.lower
        i += 1
        while i <= self.n:
            if i-1 not in self.data:
                self.data[i-1] = 0
            self.data[i-1] += x
            i += -i & i
    
    def set(self, i, x):
        self.add(i, x-self[i])
    
    def _prod(self,i):
        i -= self.lower
        res = 0
        while i > 0:
            res += self._data(i-1)
            i -= -i & i
        return res
    
    def prod(self,l,r):
        return self._prod(r) - self._prod(l)
    
    def bisect_left(self,x):
        """[0,i)の累積和を二分探索"""
        i = 1 << self.n.bit_length()-1
        val = self.e
        while not i & 1:
            if val + self._data(i-1) < x:
                val += self._data(i-1)
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1+self.lower + (val+self._data(i-1) < x)
    
    def bisect_right(self,x):
        """[0,i)の累積和を二分探索"""
        i = 1 << (self.upper - self.lower).bit_length()-1
        val = self.e
        while not i & 1:
            if val + self._data(i-1) <= x:
                val += self._data(i-1)
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1+self.lower + (val+self._data(i-1) <= x)