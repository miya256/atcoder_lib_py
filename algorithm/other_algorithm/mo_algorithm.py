class Mo:
    def __init__(self,n,query):
        """[[l1,r1],[l2,r2],...]を想定"""
        self.n = n
        self.q = len(query)
        self.query = [[i,l,r] for i,(l,r) in enumerate(query)]
        self.b = n // (self.q ** 0.5)

        self.maxn = 1 << (n-1).bit_length()

        #self.query.sort(key = lambda x:(x[1]//self.b, x[2] if (x[1]//self.b) % 2 == 0 else -x[2]))
        self.query.sort(key = self._hilbert)
    
    def _hilbert(self,x):
        l = x[1]
        r = x[2]
        d = 0
        s = self.maxn >> 1
        while s:
            rl = ((l & s) > 0)
            rr = ((r & s) > 0)
            d += s * s * ((rl * 3) ^ rr)
            if rr:
                s >>= 1
                continue
            if rl:
                l = self.maxn-1 - l
                r = self.maxn-1 - r
            l,r = r,l
            s >>= 1
        return d
    
    def execute(self):
        ans = [None]*self.q
        ptr_l, ptr_r = 0,-1
        for i,l,r in self.query:
            #l,rのindexを調整
            l -= 1
            r -= 1

            while ptr_r < r:
                ptr_r += 1
                #処理
            while ptr_l > l:
                ptr_l -= 1
                #処理
            while ptr_r > r:
                #処理
                ptr_r -= 1
            while ptr_l < l:
                #処理
                ptr_l += 1
            ans[i] = hoge