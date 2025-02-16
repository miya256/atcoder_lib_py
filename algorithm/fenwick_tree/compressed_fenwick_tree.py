from bisect import bisect_left, bisect
class CompressedFenwickTree: #座標圧縮を用いたFenwickTree
    class Shrink:
        def __init__(self,num):
            """num:出てくる数字。i番目の数字がxみたいな。l,rの数字は含めなくてよい"""
            self.num = sorted([i for i in set(num)])
            self.shr = {v:i for i,v in enumerate(self.num)}
        
        def __len__(self):
            return len(self.num)

        def original(self,shr):
            """圧縮後の値から元の値を返す"""
            return self.num[shr]

        def shrink(self,orig):
            """元の値から圧縮後の値を返す"""
            if orig not in self.shr:
                self.shr[orig] = bisect_left(self.num,orig)
            return self.shr[orig]
        
        def __call__(self,orig):
            return self.shrink(orig)
        
    def __init__(self,num,mod=None):
        self.shr = self.Shrink(num)
        self.n = len(self.shr)
        self.mod = mod
        self.tree = [0 for _ in range(self.n)]
        self.all_sum = 0
    
    def __getitem__(self,i):
        return self.prod(i,i+1)
    
    def __setitem__(self,i,value):
        self.set(i,value)
    
    def add(self, i, x):
        """i番目にxを足す"""
        self.all_sum += x
        if self.mod:
            self.all_sum %= self.mod
        i = self.shr(i)
        i += 1
        while i <= self.n:
            self.tree[i-1] += x
            if self.mod:
                self.tree[i-1] %= self.mod
            i += -i & i
    
    def set(self, i, x):
        """加えるではなく、更新"""
        self.add(i, x - self[i])

    def _prod(self, i):
        res = 0
        while i > 0:
            res += self.tree[i-1]
            if self.mod:
                res %= self.mod
            #-i&iはiの最右の1だけ1にする演算
            #これはそれが持ってる区間のサイズと等しい
            #自分が持ってるサイズ分を足し引きして移動している
            i -= -i & i
        return res

    def prod(self,l,r):
        """[l,r)"""
        l,r = self.shr(l),self.shr(r)
        s = self._prod(r) - self._prod(l)
        return s % self.mod if self.mod else s
    
    def all_prod(self):
        return self.all_sum
    
    def bisect_left(self,x):
        """[0,i)の累積和を二分探索"""
        i = 1 << self.n.bit_length()-1
        val = 0
        while not i & 1:
            if val + self.tree[i-1] < x:
                val += self.tree[i-1]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return self.shr.original(i-1 + (val + self.tree[i-1] < x))
    
    def bisect_right(self,x):
        """[0,i)の累積和を二分探索"""
        i = 1 << self.n.bit_length()-1
        val = 0
        while not i & 1:
            if val + self.tree[i-1] <= x:
                val += self.tree[i-1]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return self.shr.original(i-1 + (val + self.tree[i-1] <= x))
    
    def __str__(self):
        return f'FenwickTree {self.tree}' #とりあえずこう