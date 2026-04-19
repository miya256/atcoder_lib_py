from typing import Generic, TypeVar, Callable

M = TypeVar("MonoidElement")  # type: ignore


class DynamicSegmentTree(Generic[M]):
    """
    Attributes:
        op(x, y): xとyの二項演算（関数型）
        e       : opの単位元
        [lower, upper)の範囲を扱う

    Methods:
        get(i)    : i番目を取得
        set(i, x) : i番目をxにする
        prod(l, r): 区間[l, r)の総積
        all_prod(): 全体の積
        max_right(l, condition): condition(prod[l,j))が真であり続ける最大のjを返す
        min_left(r, condition) : condition(prod[j,r))が真であり続ける最小のjを返す
    """

    class Node:
        def __init__(self, value: M):
            self.left: DynamicSegmentTree.Node | None = None
            self.right: DynamicSegmentTree.Node | None = None
            self.value = value

    def __init__(
        self,
        op: Callable[[M, M], M],
        e: M,
        lower: int,
        upper: int,
    ) -> None:
        self._op = op
        self._e = e
        self._lower = lower
        self._upper = upper
        self._root = DynamicSegmentTree.Node(e)

    def __getitem__(self, i: int) -> M:
        """i番目を取得"""
        return self.get(i)

    def __setitem__(self, i: int, x: M) -> None:
        """i番目にxを代入"""
        self.set(i, x)

    def __repr__(self) -> str:
        indices = []
        values = []
        stack: list[tuple[DynamicSegmentTree.Node | None, int, int]] = [
            (self._root, self._lower, self._upper)
        ]
        while stack:
            node, nl, nr = stack.pop()
            if node is None:
                continue
            if nr - nl == 1:
                width = max(len(str(nl)), len(str(node.value)))
                indices.append(f"{nl:>{width}}")
                values.append(f"{node.value:>{width}}")
                continue
            mid = (nl + nr) // 2
            stack.append((node.right, mid, nr))
            stack.append((node.left, nl, mid))

        i_str = "[" + ", ".join(indices) + "]"
        v_str = "[" + ", ".join(values) + "]"
        return f"DynamicSegmentTree(\n index: {i_str}\n value: {v_str}\n default: {self._e}\n)"

    def get(self, i: int) -> M:
        """i番目を取得"""
        assert self._lower <= i < self._upper, f"index out of range: i={i}"
        node = self._root
        nl, nr = self._lower, self._upper
        while node and nr - nl > 1:
            mid = (nl + nr) // 2
            if i < mid:
                node = node.left
                nr = mid
            else:
                node = node.right
                nl = mid
        return node.value if node else self._e

    def set(self, i: int, x: M) -> None:
        """i番目にxを代入"""
        assert self._lower <= i < self._upper, f"index out of range: i={i}"
        node = self._root
        nl, nr = self._lower, self._upper
        stack = []
        while nr - nl > 1:
            stack.append(node)
            mid = (nl + nr) // 2
            if i < mid:
                if node.left is None:
                    node.left = DynamicSegmentTree.Node(self._e)
                node = node.left
                nr = mid
            else:
                if node.right is None:
                    node.right = DynamicSegmentTree.Node(self._e)
                node = node.right
                nl = mid

        node.value = x

        while stack:
            node = stack.pop()
            self._update(node)

    def prod(self, l: int, r: int) -> M:
        assert self._lower <= l <= r <= self._upper, f"invalid range: [l,r)=[{l},{r})"
        value = self._e
        stack: list[tuple[DynamicSegmentTree.Node | None, int, int]] = [
            (self._root, self._lower, self._upper)
        ]
        while stack:
            node, nl, nr = stack.pop()
            if node is None or nr <= l or r <= nl:
                continue
            elif l <= nl and nr <= r:
                value = self._op(value, node.value)
            elif nr - nl > 1:
                mid = (nl + nr) // 2
                stack.append((node.right, mid, nr))
                stack.append((node.left, nl, mid))
        return value

    def all_prod(self) -> M:
        return self._root.value

    def max_right(self, l: int, condition: Callable[[M], bool]) -> int:
        """condition(prod[l,j))が真であり続ける最大のjを返す"""
        assert self._lower <= l <= self._upper, f"index out of range: l={l}"
        value = self._e
        j = l
        stack: list[tuple[DynamicSegmentTree.Node | None, int, int]] = [
            (self._root, self._lower, self._upper)
        ]
        while stack:
            node, nl, nr = stack.pop()

            # 範囲外
            if nr <= l:
                continue

            # 完全に含まれる or 交差 だが、すべて単位元なので関係なし
            if node is None:
                j = nr
                continue

            # 範囲が完全に入る
            if l <= nl:
                tmp = self._op(value, node.value)
                if condition(tmp):
                    value = tmp
                    j = nr
                    continue
                else:
                    # conditionを満たさないならこの区間に答えがあるので
                    # この区間より右は見なくていい
                    stack = []

            # 範囲が交差 nl < l < nr
            if nr - nl > 1:
                mid = (nl + nr) // 2
                stack.append((node.right, mid, nr))
                stack.append((node.left, nl, mid))
        return j

    def min_left(self, r: int, condition: Callable[[M], bool]) -> int:
        """condition(prod[j,r))が真であり続ける最小のjを返す"""
        assert self._lower <= r <= self._upper, f"index out of range: r={r}"
        value = self._e
        j = r
        stack: list[tuple[DynamicSegmentTree.Node | None, int, int]] = [
            (self._root, self._lower, self._upper)
        ]
        while stack:
            node, nl, nr = stack.pop()

            # 範囲外
            if r <= nl:
                continue

            # 完全に含まれる or 交差 だが、すべて単位元なので関係なし
            if node is None:
                j = nl
                continue

            # 範囲が完全に入る
            if nr <= r:
                tmp = self._op(node.value, value)
                if condition(tmp):
                    value = tmp
                    j = nl
                    continue
                else:
                    stack = []

            # 範囲が交差 nl < r < nr
            if nr - nl > 1:
                mid = (nl + nr) // 2
                stack.append((node.left, nl, mid))
                stack.append((node.right, mid, nr))
        return j

    def _update(self, node: "DynamicSegmentTree.Node") -> None:
        if node.left and node.right:
            node.value = self._op(node.left.value, node.right.value)
        elif node.left:
            node.value = node.left.value
        elif node.right:
            node.value = node.right.value
        else:
            node.value = self._e
