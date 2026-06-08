from library.graph.tree.tree import Tree


class LCA(Tree):
    def __init__(self, n: int) -> None:
        super().__init__(n)
        self._logn = n.bit_length()
        self._ancestor = [[-1] * n for _ in range(self._logn)]
        self._depth = [0] * n
        self._dist = [0] * n
        self._built = False

    def _dfs(self, root: int) -> None:
        stack = [root]
        while stack:
            u = stack.pop()
            for v, w in self(u):
                if v == self._ancestor[0][u]:
                    continue
                self._ancestor[0][v] = u
                self._depth[v] = self._depth[u] + 1
                self._dist[v] = self._dist[u] + w
                stack.append(v)

    def build(self, root: int) -> None:
        self._built = True
        self._dfs(root)
        for i in range(1, self._logn):
            for s in range(self.n):
                t = self._ancestor[i - 1][s]
                if t == -1:
                    self._ancestor[i][s] = -1
                else:
                    self._ancestor[i][s] = self._ancestor[i - 1][t]

    def parent(self, v: int) -> int:
        """v の親"""
        assert self._built
        return self._ancestor[0][v]

    def ancestor(self, v: int, k: int) -> int:
        """v から親方向に k 回たどった先の頂点"""
        assert self._built
        for i in range(self._logn):
            if k >> i & 1:
                v = self._ancestor[i][v]
        return v

    def lca(self, u: int, v: int) -> int:
        """u, v の最小共通祖先"""
        assert self._built
        if self._depth[u] > self._depth[v]:
            u, v = v, u

        # v の深さを u に合わせる
        v = self.ancestor(v, self._depth[v] - self._depth[u])

        # 一致したらそれが答え
        if u == v:
            return u

        # 一致しないぎりぎりまで親へたどり、最後に1つだけ上にやって答え
        for i in range(self._logn - 1, -1, -1):
            if self._ancestor[i][u] == self._ancestor[i][v]:
                continue
            u = self._ancestor[i][u]
            v = self._ancestor[i][v]
        return self._ancestor[0][u]

    def dist(self, u: int, v: int) -> int:
        """u, v 間の距離"""
        assert self._built
        return self._dist[u] + self._dist[v] - 2 * self._dist[self.lca(u, v)]
