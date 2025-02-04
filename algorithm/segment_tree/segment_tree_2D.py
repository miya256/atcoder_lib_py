class SegmentTree:
    def __init__(self,op,e,data):
        """演算, 単位元, list or len"""
        if isinstance(data,int):
            data = [e for _ in range(data)]
        self.n = len(data)
        self.op = op
        self.e = e
        self.size = 1 << (len(data)-1).bit_length()#最下段の長さ
        self.tree = [e for _ in range(self.size*2)]#tree[1]が最上段,tree[size]が元のdata[0]
        self._build(data)
    
    def _build(self,data):
        for i,val in enumerate(data):
            self.tree[i+self.size] = val
        for i in range(self.size-1,0,-1):
            self.tree[i] = self.op(self.tree[2*i], self.tree[2*i+1])
    
    def __getitem__(self,i):
        return self.tree[i+self.size]
    
    def __setitem__(self,i,x):
        self.set(i,x)
    
    def set(self,p,x):
        """p番目にxを代入"""
        p += self.size
        self.tree[p] = x
        while p:
            p >>= 1
            self.tree[p] = self.op(self.tree[2*p], self.tree[2*p+1])
    
    def prod(self,l,r):
        lt, rt = self.e, self.e
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
    
    def max_right(self,l,f):
        """prod[l,j)でfuncを満たす最大のjを返す"""
        if l == self.n:
            return self.n
        
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
                return l - self.size
            val = self.op(val,self.tree[l])#満たすなら確定する
            l += 1#右に移動
            if l & -l == l:#f(prod(l,n)) = Trueなら(lが2の累乗)
                return self.n#dataの一番右を返す
    
    def min_left(self,r,f):
        """prod[j,r)でfuncを満たす最小のjを返す"""
        if r == 0:
            return 0
        
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
                return r - self.size
            r -= 1
            val = self.op(val,self.tree[r])
            if r & -r == r:#f(prod(0,r)) = Trueなら(rが2の累乗)
                return 0
    
    def __str__(self):
        return f'SegmentTree {self.tree[self.size:self.size+self.n]}'

class SegmentTree2D:
    def __init__(self,op,e,data):
        self.op = op
        self.e = e
        self.h = len(data)
        self.w = len(data[0])
        self.size = 1 << (self.h-1).bit_length()
        self.tree = [SegmentTree(op,e,self.w) for _ in range(self.size*2)]
        self._build(data)
    
    def _build(self,data):
        for i in range(self.h):
            self.tree[i+self.size] = SegmentTree(self.op,self.e,data[i])
        for i in range(self.size-1,0,-1):
            tmp = [self.e for _ in range(self.w)]
            for j in range(self.w):
                tmp[j] = self.op(self.tree[2*i][j], self.tree[2*i+1][j])
            self.tree[i] = SegmentTree(self.op,self.e,tmp)

    def set(self,x,y,val):
        x += self.size
        self.tree[x][y] = val
        while x:
            x >>= 1
            self.tree[x][y] = self.op(self.tree[2*x][y], self.tree[2*x+1][y])
    
    def prod(self,l,r):
        """(lx,ly),(rx,ry)"""
        lx,ly = l
        rx,ry = r
        lt, rt = self.e, self.e
        lx += self.size
        rx += self.size
        while lx < rx:
            if lx & 1:
                lt = self.op(lt,self.tree[lx].prod(ly,ry))
                lx += 1
            if rx & 1:
                rx -= 1
                rt = self.op(self.tree[rx].prod(ly,ry),rt)
            lx >>= 1
            rx >>= 1
        return self.op(lt,rt)