class LowestCommonAncestor:
    def __init__(self,n):
        """
        n:頂点数
        k:2**k回
        tree:木(隣接リスト)
        dp:状態sから、2**i回遷移したあとの状態
        depth:深さ
        """
        self.n = n
        self.k = n.bit_length()
        self.tree = [[] for _ in range(n)]
        self.dp = [[0]*n for _ in range(self.k)]
        self.depth = [0]*n
        self.called = False
    
    def add_edge(self,u,v):
        self.tree[u].append(v)
        self.tree[v].append(u)
    
    def _dfs(self,v):
        stack = [(v,-1)]
        while stack:
            v,par = stack.pop()
            for nv in self.tree[v]:
                if nv != par:
                    self.dp[0][nv] = v
                    self.depth[nv] = self.depth[v]+1
                    stack.append((nv,v))
    
    def build(self):
        self.called = True
        self._dfs(0)
        for i in range(1,self.k):
            for s in range(self.n):
                self.dp[i][s] = self.dp[i-1][self.dp[i-1][s]]

    def lca(self,u,v):
        """u,vのLCA"""
        assert self.called,"buildを実行してください"
        if self.depth[u] < self.depth[v]: u,v = v,u
        for i in range((self.depth[u]-self.depth[v]).bit_length()):
            if ((self.depth[u]-self.depth[v])>>i)&1:
                u = self.dp[i][u]
        if u == v:
            return u
        for i in range(self.k-1,-1,-1):
            if self.dp[i][u] == self.dp[i][v]:
                continue
            u = self.dp[i][u]
            v = self.dp[i][v]
        return self.dp[0][u]