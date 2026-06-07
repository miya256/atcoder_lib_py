from library.graph.tree.tree import Tree
from library.graph.tree.euler_tour import euler_tour
from library.range_query.sparse_table import SparseTable


class AuxiliaryTree(Tree):
    """
    木の座標圧縮 O(KlogN)
    """

    def __init__(self, n: int):
        super().__init__(n)
        self._in_time = []
        self._out_time = []
        self._visit = []
        self._depth = []
        self._sp = None
        self._built = False

    def build(self, root: int) -> None:
        """前処理 EulerTour と SparseTable"""
        self._built = True
        _, in_time, out_time, visit, *_, depth = euler_tour(self, root)
        sp = SparseTable(min, depth)
        self._in_time = in_time
        self._out_time = out_time
        self._visit = visit
        self._depth = depth
        self._sp = sp

    def _lca(self, u: int, v: int) -> int:
        assert self._sp
        l = min(self._in_time[u], self._in_time[v])
        r = max(self._out_time[u], self._out_time[v])
        _, step = self._sp.prod(l, r)
        return self._visit[step]

    def build_aux_tree(self, nodes: list[int]) -> dict[int, int]:
        """
        与えられた頂点とそのLCAからなる木
        親のdictを返す。根の親は-1
        """
        assert self._built

        # LCAを追加して、行きがけ順にソート
        nodes.sort(key=lambda x: self._in_time[x])
        for i in range(len(nodes) - 1):
            lca = self._lca(nodes[i], nodes[i + 1])
            nodes.append(lca)

        nodes.sort(key=lambda x: self._in_time[x])

        stack = []
        parent = {}
        prev = -1
        for v in nodes:
            if prev == v:
                continue
            while stack and self._out_time[stack[-1]] < self._in_time[v]:
                stack.pop()
            if stack:
                parent[v] = stack[-1]
            stack.append(v)
            prev = v
        parent[stack[0]] = -1
        return parent
