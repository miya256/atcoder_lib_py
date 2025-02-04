class Heap:
    def __init__(self,h=[],func=lambda x,y:x<=y,e=float('inf')):
        """
        func : 親をx、子をyとしたときに、その条件を満たしているかどうか
        e    : func(x,e)が常に真となるもの
        
        """
        self.h = h
        self.func = func
        self.e = e
        for i in range(len(h)//2-1,-1,-1):
            k = i
            while True:
                li = 2*k+1
                ri = 2*k+2
                lv = self.h[li] if li < len(h) else e
                rv = self.h[ri] if ri < len(h) else e
                if lv == rv == e:
                    break
                elif func(h[k],lv) and func(h[k],rv):
                    break
                elif func(lv,rv):
                    self.h[k],self.h[li] = self.h[li],self.h[k]
                    k = li
                else:
                    self.h[k],self.h[ri] = self.h[ri],self.h[k]
                    k = ri

    def hpush(self,v):
        self.h.append(v)
        nowi = len(self.h)-1
        while nowi > 0:
            pari = (nowi-1)//2
            if self.func(self.h[pari],self.h[nowi]):
                break
            self.h[pari],self.h[nowi] = self.h[nowi],self.h[pari]
            nowi = pari

    def hpop(self):
        res = self.h[0]
        self.h[0] = self.h[-1]
        self.h.pop()
        nowi = 0
        while nowi < len(self.h):
            li = 2*nowi+1
            ri = 2*nowi+2
            lv = self.h[li] if li < len(self.h) else self.e
            rv = self.h[ri] if ri < len(self.h) else self.e
            nowv = self.h[nowi]
            if li >= len(self.h) and ri >= len(self.h):
                break
            elif li == len(self.h)-1 and not self.func(nowv,lv):
                self.h[nowi],self.h[li] = lv,nowv
                nowi = li
            elif self.func(nowv,lv) and self.func(nowv,rv):
                break
            elif self.func(lv,rv):
                self.h[nowi],self.h[li] = lv,nowv
                nowi = li
            else:
                self.h[nowi],self.h[ri] = rv,nowv
                nowi = ri
        return res
