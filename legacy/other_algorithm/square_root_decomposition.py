class SqrtDecomposition:
    def __init__(self,op,e,data):
        self.op = op
        self.e = e
        self.n = data if isinstance(data,int) else len(data)
        self.rn = int(n**0.5)
        self.chunk_count = (n+self.rn-1)//self.rn
        self.data = [e] * self.rn * self.chunk_count
        self.chunk_prod = [e] * self.chunk_count
        if isinstance(data,list):
            self._build(data)
    
    def _build(self,data):
        for i in range(0,self.n,self.rn):
            val = self.e
            for j in range(self.rn):
                self.data[i+j] = data[min(i+j,self.n-1)]
                val = self.op(val,self.data[i+j])
            self.chunk_prod.append(val)

    def chunk(self,p):
        """data[p]の属するチャンク"""
        return p//self.rn
    
    def left(self,p):
        """p番目のチャンクの区間[l,r)のl"""
        return self.rn*p

    def right(self,p):
        """p番目のチャンクの区間[l,r)のr"""
        return self.rn*(p+1)

    def set(self,p,x):
        """data[p]をxに"""
        self.data[p] = x
        cnk = self.chunk(p)
        l = self.left(cnk)
        r = self.right(cnk)
        val = self.e
        for i in range(l,r):
            val = self.op(val,self.data[i])
        self.chunk_prod[cnk] = val
    
    def prod(self,l,r):
        res = self.e
        #同じブロックなら[l,r)を全部みる
        if self.chunk(l) == self.chunk(r):
            for i in range(l,r):
                res = self.op(res,self.data[i])
            return res
        #左、中央、右を求める
        lt = mid = rt = self.e
        for i in range(l,self.right(self.chunk(l))):
            lt = self.op(lt,self.data[i])
        for i in range(self.left(self.chunk(r)),r):
            rt = self.op(rt,self.data[i])
        for i in range(self.chunk(l)+1,self.chunk(r)):
            mid = self.op(mid,self.chunk_prod[i])
        res = self.op(lt,rt)
        res = self.op(res,mid)
        return res
    
    def __str__(self):
        data = []
        for i in range(0,self.n,self.rn):
            data.append([])
            for j in range(self.rn):
                data[-1].append(self.data[i+j])
        return f'data {data}\nchunk {self.chunk_prod}'

n,q = map(int,input().split())
a = SqrtDecomposition(lambda x,y:x+y,0,n)

for _ in range(q):
    query = list(map(int,input().split()))
    if query[0] == 1:
        pos,x = query[1:]
        a.set(pos-1,x)
    else:
        l,r = query[1:]
        print(a.prod(l-1,r-1))
    print(a)