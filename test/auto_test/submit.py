class Graph:
    """
    CSR形式
    buildを手動で呼び出す必要がある

    Attributes:
        n    : 頂点数
        m    : 辺数
        edges: 辺(u,v,w)

    Methods:
        build                : CSRの配列をつくる
        add_edge             : u -> v に重み w の 有向辺 を張る
        edge                 : id番目の辺
        neighbors            : 隣接頂点 __getitem__ に割り当て
        neighbors_with_weight: 重み付き隣接頂点 __call__ に割り当て
    """
    def __init__(self, n: int, m: int) -> None:
        self.n = n
        self.m = m
        self.edges: list[tuple[int, int, int]] = []
        self._start = [0] * (n+1)
        self._adj: list[int] | None = None
        self._weight: list[int] | None = None

    def __len__(self) -> int:
        """頂点数"""
        return self.n

    def __getitem__(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self.neighbors(v)

    def __call__(self, v: int) -> list[tuple[int, int]]:
        """vに隣接する頂点のリスト（重み付き）"""
        return self.neighbors_with_weight(v)

    def build(self) -> None:
        """グラフを作成"""
        self._adj = [0] * len(self.edges)
        self._weight = [0] * len(self.edges)
        for i in range(self.n):
            self._start[i+1] += self._start[i]
        for u, v, w in self.edges:
            self._start[u] -= 1
            self._adj[self._start[u]] = v
            self._weight[self._start[u]] = w

    def add_edge(self, u: int, v: int, w: int = 1) -> int:
        """u -> v に重み w の 有向辺 を張る"""
        self.edges.append((u, v, w))
        self._start[u] += 1
        return len(self.edges) - 1

    def edge(self, id: int) -> tuple[int, int, int]:
        """辺id"""
        return self.edges[id]

    def neighbors(self, v: int) -> list[int]:
        """vに隣接する頂点のリスト"""
        return self._adj[self._start[v]: self._start[v+1]]

    def neighbors_with_weight(self, v: int) -> list[tuple[int, int]]:
        """v に隣接する頂点のリスト（重み付き）"""
        return list(zip(self._adj[self._start[v]: self._start[v+1]], self._weight[self._start[v]: self._start[v+1]]))


class Diameter(Graph):
    def __init__(self, n: int) -> None:
        super().__init__(n, n-1)
    
    def _dfs(self, v: int, dist: list[int] | None = None) -> tuple[int, int]:
        """distを指定すればvからの距離、そうでなければ直径と端点"""
        stack = [(v, -1, 0)]
        end, diameter = -1, 0
        while stack:
            u, par, d = stack.pop()

            if dist is not None:
                dist[u] = d

            if diameter < d:
                diameter = d
                end = u

            for v, w in self(u):
                if v != par:
                    stack.append((v, u, d+w))
        
        return diameter, end
    
    def diameter(self) -> tuple[int, int, int]:
        """直径、端点1、端点2"""
        _, end1 = self._dfs(0)
        diameter, end2 = self._dfs(end1)
        return diameter, end1, end2
    
    def dist(self, v: int) -> list[int]:
        """vからの距離"""
        dist = [inf := 1<<61] * self.n
        self._dfs(v, dist)
        return dist
    

class FenwickTree:
    """
    区間の和を O(log n) で計算

    Methods:\n
        get(i)         : i番目を取得
        set(i, x)      : i番目をxにする
        add(i, x)      : i番目にxを加算
        sum(l, r)      : 区間[l, r)の和
        bisect_left(x) : 累積和配列とみなし、二分探索
        bisect_right(x): 累積和配列とみなし、二分探索
    """

    def __init__(self, data: list|int) -> None:
        if isinstance(data, int):
            data = [0 for _ in range(data)]
        self._n = len(data)
        self._data = data
        self._tree = [0] * (self._n + 1)
        self._all_sum = self._build(data)
    
    def _build(self, data: list) -> int:
        """treeを作成。すべての和を返す"""
        cum = [0] * (self._n + 1)
        for i in range(1, self._n+1):
            cum[i] = cum[i-1] + data[i-1]
            self._tree[i] = cum[i] - cum[i-(-i&i)]
        return cum[-1]
    
    def __len__(self) -> int:
        """データの大きさ"""
        return self._n
    
    def __getitem__(self, i: int) -> int:
        """i番目を取得"""
        return self.get(i)
    
    def __setitem__(self, i: int, x: int) -> None:
        """i番目をxにする"""
        self.set(i, x)
    
    def __repr__(self) -> str:
        return f'FenwickTree {self._data}'
    
    def get(self, i: int) -> int:
        """i番目を取得"""
        return self._data[i]
    
    def add(self, i: int, x: int) -> None:
        """i番目にxを加える"""
        self._data[i] += x
        self._all_sum += x
        i += 1
        while i <= self._n:
            self._tree[i] += x
            i += -i & i
    
    def set(self, i: int, x: int) -> None:
        """i番目をxにする"""
        self.add(i, x - self._data[i])
    
    def _sum(self, i: int) -> int:
        """区間[0, i)の和"""
        sum = 0
        while i > 0:
            sum += self._tree[i]
            i -= -i & i
        return sum
    
    def sum(self, l: int, r: int) -> int:
        """区間[l, r)の和"""
        return self._sum(r) - self._sum(l)
    
    def bisect_left(self, x: int) -> int:
        """区間[0, index)の和がx以上になる最小のindex"""
        i = 1 << self._n.bit_length() - 1
        value = 0
        while not i & 1:
            if i-1 < self._n and value + self._tree[i] < x:
                value += self._tree[i]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (value + self._tree[i] < x)
    
    def bisect_right(self, x: int) -> int:
        """区間[0, index)の和がx超過になる最小のindex"""
        i = 1 << self._n.bit_length()-1
        value = 0
        while not i & 1:
            if i-1 < self._n and value + self._tree[i] <= x:
                value += self._tree[i]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (value + self._tree[i] <= x)
    

from bisect import bisect_left

n1 = int(input())
t1 = Diameter(n1)
for _ in range(n1-1):
    u,v = map(lambda x:int(x)-1,input().split())
    t1.add_edge(u,v)
    t1.add_edge(v,u)
t1.build()

n2 = int(input())
t2 = Diameter(n2)
for _ in range(n2-1):
    u,v = map(lambda x:int(x)-1,input().split())
    t2.add_edge(u,v)
    t2.add_edge(v,u)
t2.build()

r1, *end1 = t1.diameter()
r2, *end2 = t2.diameter()
r = max(r1,r2)

di = [max(d1, d2) for d1,d2 in zip(t1.dist(end1[0]), t1.dist(end1[1]))]
dj = [max(d1, d2) for d1,d2 in zip(t2.dist(end2[0]), t2.dist(end2[1]))]
dj.sort()
ft = FenwickTree(dj)

ans = 0
for i in range(n1):
    idx = bisect_left(dj, r-di[i]-1) #rより小さくなる個数
    cnt = n2-idx #r以上になる個数
    ans += r * idx + (di[i]+1)*cnt + ft.sum(idx, n2)
print(ans)