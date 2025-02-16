from bisect import bisect_left, bisect
class CompressedSegmentTree:
    INF = 1<<61
    
    class Shrink:
        def __init__(self,num):
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
        
    def __init__(self,op,e,num):
        """演算, 単位元, list or len"""
        self.shr = self.Shrink(num)
        self.n = len(self.shr)
        self.op = op
        self.e = e
        self.size = 1 << (self.n-1).bit_length()#最下段の長さ
        self.tree = [e for _ in range(self.size*2)]#tree[1]が最上段,tree[size]が元のdata[0]
    
    def __getitem__(self,i):
        return self.prod(i,i+1)
    
    def set(self,p,x):
        """p番目にxを代入"""
        p = self.shr(p)
        p += self.size
        self.tree[p] = x
        while p:
            p >>= 1
            self.tree[p] = self.op(self.tree[2*p], self.tree[2*p+1])
    
    def prod(self,l,r):
        lt, rt = self.e, self.e
        l,r = self.shr(l),self.shr(r)
        l += self.size
        r += self.size
        while l < r:
            if l & 1:#右側だけなら
                lt = self.op(lt,self.tree[l])
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1:#左側だけなら
                r -= 1
                rt = self.op(self.tree[r],rt)
            l >>= 1
            r >>= 1
        return self.op(lt,rt)
    
    def all_prod(self):
        return self.tree[1]
    
    def max_right(self,l,f):
        """prod[l,j)でfuncを満たす最大のjを返す"""
        l = self.shr(l)
        if l == self.n:
            return self.shr.original(self.n-1)
        
        l += self.size
        val = self.e#確定した区間の積
        while True:
            while not l & 1:#右ノードになるまで親に移動
                l >>= 1
            if not f(self.op(val,self.tree[l])):
                while l < self.size:#下まで
                    l <<= 1#左の子に移動
                    if f(self.op(val,self.tree[l])):#満たすなら
                        val = self.op(val,self.tree[l])#左は確定して
                        l += 1#同じ段の右ノードに移動
                return self.shr.original(l - self.size)
            val = self.op(val,self.tree[l])#満たすなら確定する
            l += 1#右に移動
            if l & -l == l:#f(prod(l,n)) = Trueなら(lが2の累乗)
                return self.INF #dataの一番右を返す
    
    def min_left(self,r,f):
        """prod[j,r)でfuncを満たす最小のjを返す"""
        r = self.shr(r)
        if r == 0:
            return -self.INF
        
        r += self.size
        val = self.e
        while True:
            while not r & 1:
                r >>= 1
            if not f(self.op(val,self.tree[r-1])):
                while r < self.size:
                    r <<= 1
                    if f(self.op(val,self.tree[r-1])):
                        r -= 1
                        val = self.op(val,self.tree[r])
                return self.shr.original(r - self.size)
            r -= 1
            val = self.op(val,self.tree[r])
            if r & -r == r:#f(prod(0,r)) = Trueなら(rが2の累乗)
                return -self.INF
    
    def __str__(self):
        return f'SegmentTree {self.tree[self.size:self.size+self.n]}'

