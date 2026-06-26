from library.graph.tree.tree import Tree


class HLD(Tree):
    """
    重軽分解

    buildは分解したあとの辺の重みを返している
    それを SegmentTree とかに渡そう
    prodやapply範囲は、edge_path_rangesメソッドが求めてくれる
    頂点の重みにしたい場合は、self._vertexをもとに重みを並び替えよう
    """

    def __init__(self, n: int):
        super().__init__(n)
        self._parent = [-1] * n
        self._depth = [-1] * n
        self._size = [0] * n
        self._heavy_child = [-1] * n
        self._heavy_edge_weight = [-1] * n

        self._top = [-1] * n
        self._idx = [-1] * n
        self._vertex = [-1] * n

    def build(self, root: int) -> list[int]:
        self._make_heavy(root)
        edge_weight = self._make_path(root)
        # 左が深いほうが扱いやすいので逆にする
        edge_weight = edge_weight[::-1]
        self._vertex = self._vertex[::-1]
        self._idx = [self.n - i - 1 for i in self._idx]
        return edge_weight

    def _make_heavy(self, root: int) -> None:
        stack = [(root, -1, -1)]
        while stack:
            u, p, w = stack.pop()
            if u >= 0:
                self._parent[u] = p
                self._depth[u] = self._depth[p] + 1
                self._size[u] += 1
                for v, w in self(u):
                    if v != p:
                        stack.append((~u, v, w))
                        stack.append((v, u, w))
            else:
                ch = p
                par = ~u
                # chの部分木が現時点でのheavy_childの部分木より大きいなら更新
                if (
                    self._heavy_child[par] == -1
                    or self._size[ch] > self._size[self._heavy_child[par]]
                ):
                    self._heavy_child[par] = ch
                    self._heavy_edge_weight[par] = w
                self._size[par] += self._size[ch]

    def _make_path(self, root: int) -> list[int]:
        edge_weight = []
        stack = [(root, -1, 0)]
        while stack:
            u, par, w = stack.pop()
            self._top[u] = (
                self._top[par] if par != -1 and u == self._heavy_child[par] else u
            )
            self._idx[u] = len(edge_weight)
            self._vertex[self._idx[u]] = u
            edge_weight.append(w)
            for v, w in self(u):
                if v == par or v == self._heavy_child[u]:
                    continue
                stack.append((v, u, w))
            if self._heavy_child[u] != -1:
                v, w = self._heavy_child[u], self._heavy_edge_weight[u]
                stack.append((v, u, w))
        return edge_weight

    def index(self, u: int, v: int) -> int:
        """edge_weightにおける、辺uvの重みに対応するindex"""
        ch = u if self._parent[u] == v else v
        return self._idx[ch]

    def vertex_path_ranges(self, u: int, v: int) -> list[tuple[int, int]]:
        """path u-v のvertext_weight上での複数区間を返す"""
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
        """path u-v のedge_weight上での複数区間を返す"""
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

    def ancestor(self, v: int, d: int) -> int:
        """vの祖先であって、深さがdの頂点"""
        if self._depth[v] < d:
            return -1
        while True:
            top = self._top[v]
            if self._depth[top] <= d:
                depth_diff = self._depth[v] - d
                return self._vertex[self._idx[v] + depth_diff]
            v = self._parent[top]

    def lca(self, u: int, v: int) -> int:
        while True:
            ui, vi = self._idx[u], self._idx[v]
            # 同じ heavy path 上なら浅いほうがlca
            if self._top[u] == self._top[v]:
                return u if self._depth[u] < self._depth[v] else v

            u_top, v_top = self._top[u], self._top[v]
            if self._depth[u_top] < self._depth[v_top]:
                u, v = v, u
                ui, vi = vi, ui
                u_top, v_top = v_top, u_top
            # 深いほうを処理して上に
            u = self._parent[u_top]
