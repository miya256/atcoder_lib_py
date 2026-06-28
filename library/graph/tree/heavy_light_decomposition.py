from library.graph.tree.tree import Tree


class HLD(Tree):
    """
    重軽分解

    Attributes:
        parent     : 頂点 v の親
        depth      : 頂点 v の深さ
        size       : 部分木 v の頂点数
        heavy_child: 子の中で部分木の頂点数が最大であるもの
        top        : 頂点 v を含む heavy path 上で最も根に近い頂点
        order      : heavy path の順で並べた頂点番号
        idx        : order 内の v の index

    Methods:
        ancestor(v, d)          : vの祖先であって、深さがdの頂点
        lca(u, v)               : u, v の最近共通祖先
        path_length(u, v)       : u-v 間の距離（辺の重みを1とした場合）
        jump(u, v, k)           : u-v パス上で u から数えて k 番目の頂点 (0番目はu)
        is_on_path(u, v, x)     : 頂点 x が パスu-v 上に存在するか

        make_edge_weight_array()               : セグメント木などにいれるよう、辺の重みの配列をつくる
        make_vertex_weight_array(vertex_weight): セグメント木などにいれるよう、頂点の重み配列をつくる

        vertex_path_ranges(u, v)  : パス u-v の頂点配列上での複数区間を返す
        edge_path_ranges(u, v)    : パス u-v の辺配列上での複数区間を返す
        vertex_subtree_range(v)   : 部分木 v の頂点配列上での区間
        edge_subtree_range(v)     : 部分木 v の辺配列上での区間
    """

    def __init__(self, n: int):
        super().__init__(n)
        self._parent = [-1] * n
        self._depth = [-1] * n
        self._size = [0] * n
        self._heavy_child = [-1] * n

        self._top = [-1] * n
        self._idx = [-1] * n
        self._order = []
        self._built = False

    def build(self, root: int):
        if self._built:
            return
        self._make_heavy(root)
        self._make_path(root)
        # 左が深いほうが扱いやすいので逆にする
        self._order = self._order[::-1]
        self._idx = [self.n - i - 1 for i in self._idx]
        self._built = True

    def _make_heavy(self, root: int) -> None:
        """
        heavy childを求める
        同時に、親、深さ、部分木サイズなども求める
        """
        stack = [(root, -1)]
        while stack:
            u, p = stack.pop()
            if u >= 0:
                self._parent[u] = p
                self._depth[u] = self._depth[p] + 1
                self._size[u] += 1
                for v in self[u]:
                    if v != p:
                        stack.append((~u, v))
                        stack.append((v, u))
            else:
                ch = p
                par = ~u
                # chの部分木が現時点でのheavy_childの部分木より大きいなら更新
                if (
                    self._heavy_child[par] == -1
                    or self._size[ch] > self._size[self._heavy_child[par]]
                ):
                    self._heavy_child[par] = ch
                self._size[par] += self._size[ch]

    def _make_path(self, root: int):
        stack = [(root, -1)]
        while stack:
            u, par = stack.pop()
            self._top[u] = (
                self._top[par] if par != -1 and u == self._heavy_child[par] else u
            )
            self._idx[u] = len(self._order)
            self._order.append(u)
            for v in self[u]:
                if v == par or v == self._heavy_child[u]:
                    continue
                stack.append((v, u))
            if self._heavy_child[u] != -1:
                stack.append((self._heavy_child[u], u))

    def ancestor(self, v: int, d: int) -> int | None:
        """vの祖先であって、深さがdの頂点"""
        assert self._built
        if self._depth[v] < d:
            return None
        while True:
            top = self._top[v]
            if self._depth[top] <= d:
                depth_diff = self._depth[v] - d
                return self._order[self._idx[v] + depth_diff]
            v = self._parent[top]

    def lca(self, u: int, v: int) -> int:
        """u, v の最近共通祖先"""
        assert self._built
        while True:
            # 同じ heavy path 上なら浅いほうがlca
            if self._top[u] == self._top[v]:
                return u if self._depth[u] < self._depth[v] else v

            u_top, v_top = self._top[u], self._top[v]
            if self._depth[u_top] < self._depth[v_top]:
                v = self._parent[v_top]
            else:
                u = self._parent[u_top]

    def path_length(self, u: int, v: int) -> int:
        """u-v 間の距離（辺の重みを1とした場合）"""
        assert self._built
        w = self.lca(u, v)
        return self._depth[u] + self._depth[v] - 2 * self._depth[w]

    def jump(self, u: int, v: int, k: int) -> int | None:
        """u-v パス上で u から数えて k 番目の頂点 (0番目はu)"""
        assert self._built
        path_length = self.path_length(u, v)
        if k > path_length:
            return None
        w = self.lca(u, v)
        if self._depth[u] - self._depth[w] >= k:
            return self.ancestor(u, self._depth[u] - k)
        else:
            return self.ancestor(v, self._depth[v] - path_length + k)

    def is_on_path(self, u: int, v: int, x: int) -> bool:
        """頂点 x が パスu-v 上に存在するか"""
        assert self._built
        return self.path_length(u, x) + self.path_length(x, v) == self.path_length(u, v)

    def make_edge_weight_array(self) -> list[int]:
        """辺の重みの配列をつくる (Segment Tree とかに入れる用)"""
        edge_weight = [0] * (self.n - 1)
        for u in range(self.n):
            for v, w in self(u):
                ch = u if self._parent[u] == v else v
                edge_weight[self._idx[ch]] = w
        return edge_weight

    def make_vertex_weight_array(self, vertex_weight: list[int]) -> list[int]:
        """頂点の重みの配列をつくる (Segment Tree とかに入れる用)"""
        return [vertex_weight[self._order[i]] for i in range(self.n)]

    def vertex_path_ranges(self, u: int, v: int) -> list[tuple[int, int]]:
        """パス u-v の頂点配列上での複数区間を返す"""
        assert self._built
        lr = []
        while True:
            ui, vi = self._idx[u], self._idx[v]
            if self._top[u] == self._top[v]:
                # 深いほうが左
                if self._depth[u] < self._depth[v]:
                    ui, vi = vi, ui
                lr.append((ui, vi + 1))
                return lr

            u_top, v_top = self._top[u], self._top[v]
            if self._depth[u_top] < self._depth[v_top]:
                u, v = v, u
                ui, vi = vi, ui
                u_top, v_top = v_top, u_top
            # 深いほうを処理して上に
            lr.append((ui, self._idx[u_top] + 1))
            u = self._parent[u_top]

    def edge_path_ranges(self, u: int, v: int) -> list[tuple[int, int]]:
        """パス u-v の辺配列上での複数区間を返す"""
        assert self._built
        lr = []
        while True:
            ui, vi = self._idx[u], self._idx[v]
            if self._top[u] == self._top[v]:
                # 深いほうが左
                if self._depth[u] < self._depth[v]:
                    ui, vi = vi, ui
                lr.append((ui, vi))
                return lr

            u_top, v_top = self._top[u], self._top[v]
            if self._depth[u_top] < self._depth[v_top]:
                u, v = v, u
                ui, vi = vi, ui
                u_top, v_top = v_top, u_top
            # 深いほうを処理して上に
            lr.append((ui, self._idx[u_top] + 1))
            u = self._parent[u_top]

    def vertex_subtree_range(self, v: int) -> tuple[int, int]:
        """部分木 v の頂点配列上での区間"""
        assert self._built
        l = self._idx[v] - self._size[v] + 1
        r = self._idx[v] + 1
        return l, r

    def edge_subtree_range(self, v: int) -> tuple[int, int]:
        """部分木 v の辺配列上での区間"""
        assert self._built
        l = self._idx[v] - self._size[v] + 1
        r = self._idx[v]
        return l, r
