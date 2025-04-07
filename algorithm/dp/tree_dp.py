from copy import deepcopy
class TreeDP:
    def __init__(self,n,propagate,merge,init):
        """
        n: 頂点数
        propagate(pdata,cdata,par,ch,w): 子から親への遷移
        merge(data1,data2,v): 根が同じ木の合成
        init: dpの初期値（葉のみの場合の答え）
        """
        self.n = n
        self.propagate = propagate
        self.merge = merge
        self.init = init
        self.tree = [[] for _ in range(n)]
        self.dp1 = [deepcopy(init) for _ in range(n)] #vを根とする部分木について
        self.dp2 = [deepcopy(init) for _ in range(n)] #部分木ではないほう(v含む)について
        self.ans = [0]*n #vを根としたときの全体の答え
    
    def add_edge(self,u,v,w=1):
        self.tree[u].append((v,w))
        self.tree[v].append((u,w))

    def _dfs1(self,v):
        stack = [(v,-1,-1)]
        while stack:
            v,par,w = stack.pop()
            if v >= 0:
                for nv,w in self.tree[v]:
                    if nv != par:
                        stack.append((~nv,v,w))
                        stack.append((nv,v,w))
            else:
                ch = ~v
                self.dp1[par] = self.propagate(self.dp1[par],self.dp1[ch],par,ch,w)
    
    def _dfs2(self,v):
        stack = [(~v,-1),(v,-1)]
        while stack:
            v,par = stack.pop()
            if v >= 0:
                acc_l = [deepcopy(self.init) for _ in range(len(self.tree[v])+1)]
                acc_r = [deepcopy(self.init) for _ in range(len(self.tree[v])+1)]
                for i,(nv,w) in enumerate(self.tree[v]):
                    acc_l[i+1] = acc_l[i]
                    if nv != par:
                        acc_l[i+1] = self.propagate(acc_l[i],self.dp1[nv],v,nv,w)
                for i,(nv,w) in enumerate(self.tree[v][::-1],1):
                    acc_r[-i-1] = acc_r[-i]
                    if nv != par:
                        acc_r[-i-1] = self.propagate(acc_r[-i],self.dp1[nv],v,nv,w)
                
                for i,(nv,w) in enumerate(self.tree[v]):
                    if nv != par:
                        self.dp2[nv] = self.propagate(self.dp2[nv], self.merge(self.dp2[v], self.merge(acc_l[i], acc_r[i+1], v), v),nv,v,w)
                        stack.append((~nv,v))
                        stack.append((nv,v))
            else:
                v = ~v
                self.ans[v] = self.merge(self.dp1[v],self.dp2[v],v)
        
    def tree_dp(self,v):
        """vを根としたときの答え"""
        self._dfs1(v)
        return self.dp1
    
    def rerooting(self):
        """0~nを根としたときの答え"""
        self._dfs1(0)
        self._dfs2(0)
        return self.ans

def propagate(pdata,cdata,par,ch,w):
    """子から親への遷移(ミュータブルな場合はコピーする)"""
    return max(pdata,cdata+w)

def merge(data1,data2,v):
    """vを根とする部分木同士を合成"""
    return max(data1,data2)