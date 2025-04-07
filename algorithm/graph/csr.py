class CSR:
    def __init__(self,n,edge=[]):
        self.n = n
        self.val = []
        self.start = [] #i行目の開始位置
        self.edge = edge
    
    def add_edge(self,u,v,w=1):
        self.edge.append((u,v,w))
    
    def build(self):
        val = [None] * len(self.edge)
        start = [0] * (self.n+1)
        for u,_,_ in self.edge:
            start[u] += 1
        for i in range(self.n):
            start[i+1] += start[i]
        for u,v,w in self.edge:
            start[u] -= 1
            val[start[u]] = (v,w)
        self.val = val
        self.start = start
    
    def __getitem__(self,i):
        return self.val[self.start[i]:self.start[i+1]]