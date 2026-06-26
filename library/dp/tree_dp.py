from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class TreeDP(Generic[T]):
    def __init__(
        self,
        n: int,
        merge1: Callable[[T, T, tuple[int, int, int]], T],
        merge2: Callable[[T, T, int], T],
        init: Callable[[int], T],
    ):
        """
        merge1: 親に子を根とする部分木をくっつける
        merge2: 同じ頂点を根とする部分木同士を合成
        init(v): v１つだけだったときの値
        dp1[v]: vを根とする部分木についての値
        dp2[v]: vを根とし、vの親を子とみなしたときの木についての値
        ans[v]: vを根としたときの木全体の答え
        """
        self._merge1 = merge1
        self._merge2 = merge2
        self._init = init

        self.n = n
        self.edges: list[tuple[int, int, int]] = []
        self._ptr = [0] * (n + 1)
        self._adj: list[int] = []
        self._weight: list[int] = []

    def _build(self):
        self._adj = [0] * len(self.edges)
        self._weight = [0] * len(self.edges)
        for i in range(self.n):
            self._ptr[i + 1] += self._ptr[i]
        for u, v, w in self.edges:
            self._ptr[u] -= 1
            self._adj[self._ptr[u]] = v
            self._weight[self._ptr[u]] = w

    def __getitem__(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self.neighbors(v)

    def __call__(self, v: int) -> list[tuple[int, int]]:
        """vに隣接する頂点のリスト（重み付き）"""
        return self.neighbors_with_weight(v)

    def add_edge(self, u: int, v: int, w: int = 1) -> None:
        """u -> v に重み w の 無向辺 を張る"""
        assert 0 <= u < self.n, f"u={u} is out of range"
        assert 0 <= v < self.n, f"v={v} is out of range"
        self.edges.append((u, v, w))
        self.edges.append((v, u, w))
        self._ptr[u] += 1
        self._ptr[v] += 1

        if len(self.edges) >= 2 * (self.n - 1):
            self._build()

    def neighbors(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self._adj[self._ptr[v] : self._ptr[v + 1]]

    def neighbors_with_weight(self, v: int) -> list[tuple[int, int]]:
        """v に隣接する頂点のリスト（重み付き）"""
        return list(
            zip(
                self._adj[self._ptr[v] : self._ptr[v + 1]],
                self._weight[self._ptr[v] : self._ptr[v + 1]],
            )
        )

    def tree_dp(self, root: int) -> T:
        """vを根としたときの答え"""
        dp1 = self._dfs1(root)
        return dp1[root]

    def rerooting(self) -> list[T]:
        dp1 = self._dfs1(0)
        dp2, ans = self._dfs2(0, dp1)
        return ans

    def _dfs1(self, root: int) -> list[T]:
        dp1 = [self._init(v) for v in range(self.n)]
        stack = [(root, -1, -1)]
        while stack:
            u, par, w = stack.pop()
            if u >= 0:
                for v, w in self(u):
                    if v != par:
                        stack.append((~v, u, w))
                        stack.append((v, u, w))
            else:
                ch = ~u
                dp1[par] = self._merge1(dp1[par], dp1[ch], (par, ch, w))
        return dp1

    def _dfs2(self, root: int, dp1: list[T]) -> tuple[list[T], list[T]]:
        dp2 = [self._init(v) for v in range(self.n)]
        ans = [self._init(v) for v in range(self.n)]
        stack = [(~root, -1), (root, -1)]
        while stack:
            u, par = stack.pop()
            if u >= 0:
                acc_l = [
                    self._init(u) for _ in range(self._ptr[u + 1] - self._ptr[u] + 1)
                ]
                acc_r = [
                    self._init(u) for _ in range(self._ptr[u + 1] - self._ptr[u] + 1)
                ]
                for i, (v, w) in enumerate(self(u)):
                    acc_l[i + 1] = acc_l[i]
                    if v != par:
                        acc_l[i + 1] = self._merge1(acc_l[i], dp1[v], (u, v, w))
                for i, (v, w) in enumerate(self(u)[::-1], 1):
                    acc_r[-i - 1] = acc_r[-i]
                    if v != par:
                        acc_r[-i - 1] = self._merge1(acc_r[-i], dp1[v], (u, v, w))

                for i, (v, w) in enumerate(self(u)):
                    if v != par:
                        dp2[v] = self._merge1(
                            dp2[v],
                            self._merge2(
                                dp2[u], self._merge2(acc_l[i], acc_r[i + 1], u), u
                            ),
                            (v, u, w),
                        )
                        stack.append((~v, u))
                        stack.append((v, u))
            else:
                u = ~u
                ans[u] = self._merge2(dp1[u], dp2[u], u)
        return dp2, ans

    def __memo__(self):
        """ABC348E
        def merge1(par, ch, edge: tuple[int, int, int]):
            return (par[0] + ch[0] + ch[1], par[1] + ch[1])

        def merge2(x, y, v: int):
            return (x[0] + y[0], x[1] + y[1] - c[v])

        def init(v: int):
            return (0, c[v])
        """
