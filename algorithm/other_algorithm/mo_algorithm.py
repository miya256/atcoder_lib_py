class Mo:
    def __init__(self, n, q, add_l, add_r, remove_l, remove_r, get):
        self.n = n
        self.q = q
        self.b = int(max(1, n/max(1, (q*2/3)**0.5)))

        self.query = [0] * q
        self.data = [0] * q

        self.add_l = add_l
        self.add_r = add_r
        self.remove_l = remove_l
        self.remove_r = remove_r
        self.get = get
    
    def _hilbert(self,x):
        maxn = 1 << (self.n-1).bit_length()
        l = x[1]
        r = x[2]
        d = 0
        s = maxn >> 1
        while s:
            rl = ((l & s) > 0)
            rr = ((r & s) > 0)
            d += s * s * ((rl * 3) ^ rr)
            if rr:
                s >>= 1
                continue
            if rl:
                l = maxn-1 - l
                r = maxn-1 - r
            l,r = r,l
            s >>= 1
        return d
    
    def add_query(self, i, l, r):
        """クエリの番号、[l, r)"""
        self.data[i] = (l<<20 | r)
        self.query[i] = ((l//self.b)<<40) + ((r if (l//self.b)&1 else -r)<<20) + i
    
    def execute(self):
        self.query.sort()
        ans = [0]*self.q
        mask = (1<<20)-1
        pl, pr = 0,0
        for lri in self.query:
            i = lri & mask
            lr = self.data[i]
            l, r = lr>>20, lr&mask
            while pl > l:
                pl -= 1
                self.add_l(pl)
            while pr < r:
                self.add_r(pr)
                pr += 1
            while pl < l:
                self.remove_l(pl)
                pl += 1
            while pr > r:
                pr -= 1
                self.remove_r(pr)
            ans[i] = self.get()
        return ans

def add_l(i):
    pass
def add_r(i):
    pass
def remove_l(i):
    pass
def remove_r(i):
    pass
def get():
    """答えを取得"""
    return