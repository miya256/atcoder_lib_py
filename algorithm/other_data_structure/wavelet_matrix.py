"""参考
https://miti-7.hatenablog.com/entry/2018/04/28/152259
https://zenn.dev/jij_inc/articles/bd2f220466346b
"""
"""
0以上のみ
だから負も扱いたいなら全体に+10**9とかして考えればよい
"""

from collections import defaultdict
from heapq import heappush,heappop
from collections import deque

class WaveletMatrix:
    class BitVector:
        def __init__(self, b):
            """bは0or1の配列"""
            self.b = b
            self.n = len(b)
            self.acc = [0] + b
            for i in range(len(b)):
                self.acc[i+1] += self.acc[i]

        def __getitem__(self, i):
            return self.b[i]
        
        def rank(self, x, i=-1):
            """[0,i)のx(0or1)の個数。iを指定しなければ全範囲"""
            return self._rank(x, i)
        
        def select(self, x, k):
            """k番目のx(0or1)のindex"""
            return self._select(x, k)
        
        def __str__(self):
            return f"BitVector({self.b})"
        
        
        def _rank(self, x, i):
            assert -1 <= i <= self.n
            assert x == 0 or x == 1

            if i == -1:
                i = self.n
            return self.acc[i] if x else i - self.acc[i]
        
        def _select(self, x, k):
            assert x == 0 or x == 1
            assert 0 < k <= self._rank(x)

            l, r = 0, len(self.b)
            while r-l > 1:
                mid = (l+r)//2
                if self._rank(x, mid) < k:
                    l = mid
                else:
                    r = mid
            return l
    
    def __init__(self, t: list):
        self.n = len(t)
        self.max_t = max(t)
        self.bitsize = (self.max_t+1).bit_length()
        self.digit_loop = list(range(self.bitsize-1,-1,-1)) #桁を上から順に
        self.idx = defaultdict(int)
        self.matrix = self._build(t)
    
    def _build(self, t):
        matrix = []
        for digit in self.digit_loop:
            matrix.append(WaveletMatrix.BitVector([i>>digit & 1 for i in t]))
            zeros = [i for i in t if not i>>digit & 1]
            ones = [i for i in t if i>>digit & 1]
            t = zeros + ones
        #最後のtにおいて、各値の開始index
        for i in range(self.n-1,-1,-1):
            self.idx[t[i]] = i
        return matrix
    
    def __len__(self):
        return self.n
    
    def get(self, i):
        """t[i]の要素を計算"""
        return self._get(i)
    
    def __getitem__(self, i):
        return self._get(i)
    
    def rank(self, x, l=0, r=-1):
        """t[l:r)におけるxの出現回数"""
        return self._rank(x, l, r)
    
    def select(self, x, k):
        """k個目のxのindex"""
        return self._select(x, k)
    
    def kthMin(self, k, l=0, r=-1):
        """t[l:r)でk番目に小さい値"""
        return self._kthMin(k, l, r)
    
    def kthMax(self, k, l=0, r=-1):
        """t[l:r)でk番目に大きい値"""
        return self._kthMax(k, l, r)
    
    def rangefreq(self, low, high, l=0, r=-1):
        """t[l:r)でlow以上high未満の個数"""
        return self._rangefreq(low, high, l, r)
    
    def prev_value(self, x, l=0, r=-1):
        """t[l:r)でx未満の最大値"""
        return self._prev_value(x, l, r)
    
    def next_value(self, x, l=0, r=-1):
        """t[l:r)でx以上の最小値"""
        return self._next_value(x, l, r)
    
    def topk(self, k, l=0, r=-1):
        """
        t[l:r)で出現回数が多い文字k個を頻度とともに返す
        同数の場合は昇順
        [(数字,出現数),...]
        """
        return self._topk(k, l, r)
    
    def sum(self, l=0, r=-1):
        """t[l:r)の合計"""
        return self._sum(l, r)
    
    def rangelist(self, low, high, l=0, r=-1):
        """t[l:r)でlow以上high未満の値を頻度とともに列挙"""
        return self._rangelist(low, high, l, r)
    
    def intersect(self, l1, r1, l2, r2):
        """
        t[l1:r1),t[l2:r2)で共通して出現する値と頻度
        [(数字,区間1の出現数,区間2の出現数),...]
        """
        return self._intersect(l1, r1, l2, r2)
    
    def __str__(self):
        return f'{[self[i] for i in range(self.n)]}'
    
    
    def _next_index(self, b, bit, i):
        if bit:
            return b.rank(0) + b.rank(1,i)
        else:
            return b.rank(0,i)
    
    def _get(self, i):
        assert 0 <= i < self.n
        res = 0
        for b, digit in zip(self.matrix,self.digit_loop):
            bit = b[i]
            res |= bit << digit
            i = self._next_index(b, bit, i)
        return res
    
    def _prefix_rank(self, x, i):
        for b,digit in zip(self.matrix, self.digit_loop):
            i = self._next_index(b, x>>digit&1, i)
        return i - self.idx[x]
    
    def _rank(self, x, l=0, r=-1):
        assert -1 <= l <= self.n and -1 <= r <= self.n
        if x > self.max_t:
            return 0
        return self._prefix_rank(x, r) - self._prefix_rank(x, l)
    
    def _select(self, x, k):
        assert 0 < k <= self._rank(x)
        i = self.idx[x] + k - 1
        for b, digit in zip(self.matrix[::-1],self.digit_loop[::-1]):
            if x >> digit & 1:
                i = b.select(1,i-b.rank(0)+1)
            else:
                i = b.select(0,i+1)
        return i
    
    def _kthMin(self, k, l, r):
        assert -1 <= l <= self.n and -1 <= r <= self.n
        assert k <= r-l or l == 0 and r == -1 and k <= self.n
        res = 0
        for b,digit in zip(self.matrix,self.digit_loop):
            cnt0 = b.rank(0,r) - b.rank(0,l)
            bit = cnt0 < k
            res |= bit<<digit
            l = self._next_index(b,bit,l)
            r = self._next_index(b,bit,r)
            if bit:
                k -= cnt0
        return res
    
    def _kthMax(self, k, l, r):
        assert -1 <= l <= self.n and -1 <= r <= self.n
        assert k <= r-l or l == 0 and r == -1 and k <= self.n
        res = 0
        for b,digit in zip(self.matrix,self.digit_loop):
            cnt1 = b.rank(1,r) - b.rank(1,l)
            bit = cnt1 >= k
            res |= bit<<digit
            l = self._next_index(b,bit,l)
            r = self._next_index(b,bit,r)
            if not bit:
                k -= cnt1
        return res
    
    def _prefix_freq(self, high, l, r):
        """t[0,r)でhigh未満の個数"""
        res = 0
        for b,digit in zip(self.matrix,self.digit_loop):
            bit = high>>digit & 1
            if bit:
                res += b.rank(0,r) - b.rank(0,l)
            l = self._next_index(b,bit,l)
            r = self._next_index(b,bit,r)
        return res
    
    def _rangefreq(self, low, high, l, r):
        return self._prefix_freq(high, l, r) - self._prefix_freq(low, l, r)
    
    def _prev_value(self, x, l, r):
        cnt = self._rangefreq(0, x, l, r)
        return self._kthMin(cnt, l, r) if cnt != 0 else None
    
    def _next_value(self, x, l, r):
        cnt = self._rangefreq(x, self.max_t+1, l, r)
        return self._kthMax(cnt, l, r) if cnt != 0 else None
    
    def _topk(self, k, l, r):
        hq = [(l-r, 0, 0, l, r)]
        res = []
        #sumで範囲を指定しない場合にk=-1となる
        while hq and (k == -1 or len(res) < k):
            _,num,i,l,r = heappop(hq)
            if i == len(self.matrix):
                res.append((num,r-l))
                continue
            l0 = self._next_index(self.matrix[i],0,l)
            r0 = self._next_index(self.matrix[i],0,r)
            l1 = self._next_index(self.matrix[i],1,l)
            r1 = self._next_index(self.matrix[i],1,r)
            num0 = num
            num1 = num | 1<<(self.bitsize-i-1)
            heappush(hq,(l0-r0,num0,i+1,l0,r0))
            heappush(hq,(l1-r1,num1,i+1,l1,r1))
        return res
    
    def _sum(self, l, r):
        return sum([num * cnt for num,cnt in self.topk(r-l,l,r)])
    
    def _rangelist(self, low, high, l, r):
        res = self._topk(r-l, l, r)
        res = [i for i in sorted(res) if low <= i[0] < high]
        return res
    
    def _intersect(self, l1, r1, l2, r2):
        dq = deque([(0,0,l1,r1,l2,r2)])
        res = []
        while dq:
            num,i,l1,r1,l2,r2 = dq.popleft()
            if i == len(self.matrix):
                res.append((num,r1-l1,r2-l2))
                continue
            l1_0 = self._next_index(self.matrix[i],0,l1)
            r1_0 = self._next_index(self.matrix[i],0,r1)
            l2_0 = self._next_index(self.matrix[i],0,l2)
            r2_0 = self._next_index(self.matrix[i],0,r2)
            l1_1 = self._next_index(self.matrix[i],1,l1)
            r1_1 = self._next_index(self.matrix[i],1,r1)
            l2_1 = self._next_index(self.matrix[i],1,l2)
            r2_1 = self._next_index(self.matrix[i],1,r2)
            num0 = num
            num1 = num | 1<<(self.bitsize-i-1)
            if l1_0 != r1_0 and l2_0 != r2_0:
                dq.append((num0,i+1,l1_0,r1_0,l2_0,r2_0))
            if l1_1 != r1_1 and l2_1 != r2_1:
                dq.append((num1,i+1,l1_1,r1_1,l2_1,r2_1))
        return res