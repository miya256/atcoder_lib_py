#加算、乗算、XOR (今わかってるのはこれ)

class FenwickTree:
    def __init__(self,op,e,inv,data):
        if isinstance(data,int):
            data = [e for _ in range(data)]
        self.n = len(data)
        self.op = op
        self.e = e
        self.inv = inv #opの逆演算(加算なら減算、乗算なら除算、XORならXOR)
        #逆演算をうまいことopから求めたい
        self.data = []
        self._build(data)
    
    def _build(self,data):
        acc = [self.e]
        for i in range(1,self.n+1):
            acc.append(self.op(acc[-1],data[i-1]))
            self.data.append(self.inv(acc[-1],acc[-1-(-i&i)]))
    
    def __getitem__(self,i):
        return self.prod(i,i+1)
    
    def add(self, i, x):
        """
        data[i]に定義されている演算をする
        data[i] = op(data[i],x)ということ
        """
        i += 1
        while i <= self.n:
            self.data[i-1] = self.op(self.data[i-1],x)
            i += -i & i
    
    def set(self, i, x):
        """加えるではなく、更新"""
        self.add(i, self.inv(x, self[i]))

    def _prod(self, i):
        res = self.e
        while i > 0:
            res = self.op(res, self.data[i-1])
            #-i&iはiの最右の1だけ1にする演算
            #これはそれが持ってる区間のサイズと等しい
            #自分が持ってるサイズ分を足し引きして移動している
            i -= -i & i
        return res

    def prod(self,l,r):
        """[l,r)"""
        return self.inv(self._prod(r),self._prod(l))
    
    def bisect_left(self,x):
        """[0,i)の累積和を二分探索"""
        i = 1 << self.n.bit_length()-1
        val = self.e
        while not i & 1:
            if self.op(val,self.data[i-1]) < x:
                val = self.op(val,self.data[i-1])
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (self.op(val,self.data[i-1]) < x)
    
    def bisect_right(self,x):
        """[0,i)の累積和を二分探索"""
        i = 1 << self.n.bit_length()-1
        val = self.e
        while not i & 1:
            if self.op(val,self.data[i-1]) <= x:
                val = self.op(val,self.data[i-1])
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (self.op(val,self.data[i-1]) <= x)
    
    def __str__(self):
        return f'FenwickTree {[self[i] for i in range(self.n)]}'