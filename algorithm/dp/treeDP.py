import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class TreeDP:
    #※dpの要素がiterableなとき、par = list(par)としないと壊れる
    #init, f1, f2は自分で定義する(いまは、重み付きの木の直径を求めるようになっている)
    def __init__(self,n):
        self.init = 0

        self.n = n
        self.graph = [[] for _ in range(n)]
        #vを根とする下側の部分木(普通の部分木)について
        self.dp1 = [self.init for _ in range(n)]
        #vを根とする上側の部分木について(v含む)
        self.dp2 = [self.init for _ in range(n)]
        self.res = [0]*n
    
    def f1(self,par,ch,w):
        """
        子から親へ
        dp1[v](par) = f(dp1[v](par), dp1[nv](ch))の計算
        """
        return max(par,ch+w)
    
    def f2(self,*a):
        """
        根が同じもの同士の演算
        f(dp2,acc_l,acc_r)
        3つとも根は同じ
        """
        return max(a)
    
    def add_edge(self,u,v,w=1):
        self.graph[u].append((v,w))
        self.graph[v].append((u,w))

    def _dfs1(self,v,par=-1):
        for nv,w in self.graph[v]:
            if nv == par:
                continue
            self._dfs1(nv,v)
            self.dp1[v] = self.f1(self.dp1[v], self.dp1[nv],w)

    def _dfs2(self,v,par=-1):
        acc_l = [self.init for _ in range(len(self.graph[v])+1)]
        acc_r = [self.init for _ in range(len(self.graph[v])+1)]
        for i,(nv,w) in enumerate(self.graph[v]):
            acc_l[i+1] = acc_l[i]
            if nv != par:
                acc_l[i+1] = self.f1(acc_l[i], self.dp1[nv],w)
        for i,(nv,w) in enumerate(self.graph[v][::-1],1):
            acc_r[-i-1] = acc_r[-i]
            if nv != par:
                acc_r[-i-1] = self.f1(acc_r[-i], self.dp1[nv],w)
        
        for i,(nv,w) in enumerate(self.graph[v]):
            if nv != par:
                self.dp2[nv] = self.f1(self.dp2[nv], self.f2(self.dp2[v], acc_l[i], acc_r[i+1]),w)
                self._dfs2(nv,v)
        
        self.res[v] = self.f2(self.dp1[v], self.dp2[v])
    
    def treedp(self,root):
        self._dfs1(root)
        return self.dp1[root]
    
    def rerooting(self):
        self._dfs1(0)
        self._dfs2(0)
        return max(self.res)