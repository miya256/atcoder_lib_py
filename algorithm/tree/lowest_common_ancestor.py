import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

class LCA:
    def __init__(self,n,tree):
        """
        n:頂点数
        k:2**k回
        tree:木(隣接リスト)
        dp:状態sから、2**i回遷移したあとの状態
        depths:深さ
        """
        self.n = n
        self.k = n.bit_length()
        self.tree = tree
        self.dp = [[0]*n for _ in range(self.k)]
        self.depths = [0]*n

        self.dfs(0)
        for i in range(1,self.k):
            for s in range(self.n):
                self.dp[i][s] = self.dp[i-1][self.dp[i-1][s]]

    def dfs(self,v,pre=-1):
        for nv in self.tree[v]:
            if nv == pre:
                continue
            self.dp[0][nv] = v
            self.depths[nv] = self.depths[v] + 1
            self.dfs(nv,v)

    def query(self,u,v):
        if self.depths[u] < self.depths[v]: u,v = v,u
        for i in range((self.depths[u]-self.depths[v]).bit_length()):
            if ((self.depths[u]-self.depths[v])>>i)&1:
                u = self.dp[i][u]
        if u == v:
            return u
        for i in range(self.k-1,-1,-1):
            if self.dp[i][u] == self.dp[i][v]:
                continue
            u = self.dp[i][u]
            v = self.dp[i][v]
        return self.dp[0][u]
