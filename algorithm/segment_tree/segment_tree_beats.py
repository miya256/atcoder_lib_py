class SegmentTreeBeats:
    INF = 1<<61

    def __init__(self,data):
        if isinstance(data,int):
            data = [0 for _ in range(data)]
        self.n = len(data)
        self.log = (len(data)-1).bit_length()
        self.size = 1 << self.log
        self.max_val = [0 for _ in range(self.size*2)]
        self.smax_val = [0 for _ in range(self.size*2)]
        self.max_cnt = [0 for _ in range(self.size*2)]
        self.min_val = [0 for _ in range(self.size*2)]
        self.smin_val = [0 for _ in range(self.size*2)]
        self.min_cnt = [0 for _ in range(self.size*2)]
        self.sum = [0 for _ in range(self.size*2)]
        self._build(data)
    
    def _build(self,data):
        for i,val in enumerate(data):
            self.sum[i+self.size] = val
            self.max_val[i+self.size] = val
            self.max_cnt[i+self.size] = 1
            self.smax_val[i+self.size] = -self.INF
            self.min_val[i+self.size] = val
            self.min_cnt[i+self.size] = 1
            self.smin_val[i+self.size] = self.INF
        for i in range(self.size-1,0,-1):
            self._update(i)
    
    def __getitem__(self,p):
        p += self.size
        for i in range(self.log,0,-1): #lazyを上から伝播させて
            self._push(p >> i)
        return self.sum[p]
    
    def __setitem__(self,p,x):
        p += self.size
        for i in range(self.log,0,-1): #lazyを上から伝播させて
            self._push(p >> i)
        self.sum[p] = x
        self.max_val[p] = x
        self.min_val[p] = x
        while p: #普通のセグ木と同じように更新
            p >>= 1
            self._update(p)
    
    def _update(self,k):
        self.sum[k] = self.sum[2*k] + self.sum[2*k+1]

        if self.max_val[2*k] > self.max_val[2*k+1]:
            self.max_val[k] = self.max_val[2*k]
            self.max_cnt[k] = self.max_cnt[2*k]
            self.smax_val[k] = max(self.smax_val[2*k],self.max_val[2*k+1])
        elif self.max_val[2*k] < self.max_val[2*k+1]:
            self.max_val[k] = self.max_val[2*k+1]
            self.max_cnt[k] = self.max_cnt[2*k+1]
            self.smax_val[k] = max(self.max_val[2*k],self.smax_val[2*k+1])
        else:
            self.max_val[k] = self.max_val[2*k]
            self.max_cnt[k] = self.max_cnt[2*k] + self.max_cnt[2*k+1]
            self.smax_val[k] = max(self.smax_val[2*k],self.smax_val[2*k+1])
        
        if self.min_val[2*k] < self.min_val[2*k+1]:
            self.min_val[k] = self.min_val[2*k]
            self.min_cnt[k] = self.min_cnt[2*k]
            self.smin_val[k] = min(self.smin_val[2*k],self.min_val[2*k+1])
        elif self.min_val[2*k] > self.min_val[2*k+1]:
            self.min_val[k] = self.min_val[2*k+1]
            self.min_cnt[k] = self.min_cnt[2*k+1]
            self.smin_val[k] = min(self.min_val[2*k],self.smin_val[2*k+1])
        else:
            self.min_val[k] = self.min_val[2*k]
            self.min_cnt[k] = self.min_cnt[2*k] + self.min_cnt[2*k+1]
            self.smin_val[k] = min(self.smin_val[2*k],self.smin_val[2*k+1])
    
    def _all_apply_chmin(self,k,f):
        """f < max_val[k]となるノードについて最大値を更新"""
        if self.max_val[k] <= f:
            return
        if f <= self.smax_val[k]:
            self.max_val[k] = f
            self._push_chmin(k)
            self._update(k)
            return
        
        self.sum[k] += (f - self.max_val[k]) * self.max_cnt[k]
        #この区間に存在する値が
        if self.max_val[k] == self.min_val[k]: #1種類のとき
            self.max_val[k] = self.min_val[k] = f
        elif self.max_val[k] == self.smin_val[k]: #2種類のとき
            self.max_val[k] = self.smin_val[k] = f
        else: #3種類以上のとき
            self.max_val[k] = f
    
    def _all_apply_chmax(self,k,f):
        """f > max_val[k]となるノードについて最小値を更新"""
        if self.min_val[k] >= f:
            return
        if f >= self.smin_val[k]:
            self.min_val[k] = f
            self._push_chmax(k)
            self._update(k)
            return
        
        self.sum[k] += (f - self.min_val[k]) * self.min_cnt[k]
        #この区間に存在する値が
        if self.min_val[k] == self.max_val[k]: #1種類のとき
            self.min_val[k] = self.max_val[k] = f
        elif self.min_val[k] == self.smax_val[k]: #2種類のとき
            self.min_val[k] = self.smax_val[k] = f
        else: #3種類以上のとき
            self.min_val[k] = f
    
    def _push_chmin(self,k):
        self._all_apply_chmin(2*k,self.max_val[k])
        self._all_apply_chmin(2*k+1,self.max_val[k])
    
    def _push_chmax(self,k):
        self._all_apply_chmax(2*k,self.min_val[k])
        self._all_apply_chmax(2*k+1,self.min_val[k])
    
    def _push(self,k):
        self._push_chmin(k)
        self._push_chmax(k)
    
    def _apply(self,l,r,f,ch_func):
        if l == r:
            return
        l += self.size
        r += self.size
        for i in range(self.log,0,-1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push(r-1 >> i)
        
        tmp_l = l
        tmp_r = r
        while l < r:
            if l & 1:
                ch_func(l,f)
                l += 1
            if r & 1:
                r -= 1
                ch_func(r,f)
            l >>= 1
            r >>= 1
        
        l = tmp_l
        r = tmp_r
        for i in range(1,self.log+1):
            if ((l >> i) << i) != l:
                self._update(l >> i)
            if ((r >> i) << i) != r:
                self._update(r-1 >> i)
    
    def _all_push(self,l,r):
        """prodの前に呼ぶ"""
        for i in range(self.log,0,-1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push(r-1 >> i)
    
    def apply_chmin(self,l,r,f):
        self._apply(l,r,f,self._all_apply_chmin)
    
    def apply_chmax(self,l,r,f):
        self._apply(l,r,f,self._all_apply_chmax)
    
    def prod_sum(self,l,r):
        if l == r:
            return 0
        l += self.size
        r += self.size
        self._all_push(l,r)
        lt = rt = 0
        while l < r:
            if l & 1:#右側だけなら
                lt += self.sum[l]
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1:#左側だけなら
                r -= 1
                rt += self.sum[r]
            l >>= 1
            r >>= 1
        return lt + rt
    
    def prod_min(self,l,r):
        if l == r:
            return self.INF
        l += self.size
        r += self.size
        self._all_push(l,r)
        lt = rt = self.INF
        while l < r:
            if l & 1:#右側だけなら
                lt = min(lt,self.min_val[l])
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1:#左側だけなら
                r -= 1
                rt = min(self.min_val[r],rt)
            l >>= 1
            r >>= 1
        return min(lt,rt)
    
    def prod_max(self,l,r):
        if l == r:
            return -self.INF
        l += self.size
        r += self.size
        self._all_push(l,r)
        lt = rt = -self.INF
        while l < r:
            if l & 1:#右側だけなら
                lt = max(lt,self.max_val[l])
                l += 1 #上は範囲外も含むから一つ右にずらす
            if r & 1:#左側だけなら
                r -= 1
                rt = max(self.max_val[r],rt)
            l >>= 1
            r >>= 1
        return max(lt,rt)
    
    def __str__(self):
        return f'{[self[i] for i in range(self.n)]}'