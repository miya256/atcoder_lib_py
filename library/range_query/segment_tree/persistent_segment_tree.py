from typing import Generic, TypeVar, Callable

M = TypeVar("MonoidElement")  # type: ignore


class PersistentSegmentTree(Generic[M]):
    """
    Attributes:
        op(x, y): xとyの二項演算（関数型）
        e       : opの単位元
        [lower, upper)の範囲を扱う

    Methods:
        get(t, i)    : i番目を取得
        set(t, i, x) : i番目をxにする
        prod(t, l, r): 区間[l, r)の総積
        all_prod(t): 全体の積
        max_right(t, l, condition): condition(prod[l,j))が真であり続ける最大のjを返す
        min_left(t, r, condition) : condition(prod[j,r))が真であり続ける最小のjを返す
    """

    class Node:
        def __init__(self, value: M):
            self.left: PersistentSegmentTree.Node | None = None
            self.right: PersistentSegmentTree.Node | None = None
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
        self._roots = [PersistentSegmentTree.Node(e)]

    def __repr__(self) -> str:
        indices = []
        values = []
        stack: list[tuple[PersistentSegmentTree.Node | None, int, int]] = [
            (self._roots[-1], self._lower, self._upper)
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
        return f"PersistentSegmentTree(\n index: {i_str}\n value: {v_str}\n default: {self._e}\n)"

    def get(self, t: int, i: int) -> M:
        """時刻tのi番目を取得"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        assert self._lower <= i < self._upper, f"index out of range: i={i}"
        node = self._roots[t]
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

    def set(self, t: int, i: int, x: M) -> int:
        """時刻tのi番目にxを代入"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        assert self._lower <= i < self._upper, f"index out of range: i={i}"
        node = self._roots[t]
        nl, nr = self._lower, self._upper
        stack = []
        path = []
        while nr - nl > 1:
            mid = (nl + nr) // 2
            if i < mid:
                stack.append(node.right if node else None)
                path.append(0)
                if node:
                    node = node.left
                nr = mid
            else:
                stack.append(node.left if node else None)
                path.append(1)
                if node:
                    node = node.right
                nl = mid

        new = PersistentSegmentTree.Node(x)

        while stack and path:
            par = PersistentSegmentTree.Node(self._e)
            ch = stack.pop()
            if path.pop() == 0:
                par.left, par.right = new, ch
            else:
                par.left, par.right = ch, new
            self._update(par)
            new = par
        self._roots.append(new)
        return self.latest_t

    def prod(self, t: int, l: int, r: int) -> M:
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        assert self._lower <= l <= r <= self._upper, f"invalid range: [l,r)=[{l},{r})"
        value = self._e
        stack: list[tuple[PersistentSegmentTree.Node | None, int, int]] = [
            (self._roots[t], self._lower, self._upper)
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

    def all_prod(self, t: int) -> M:
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        return self._roots[t].value

    def max_right(self, t: int, l: int, condition: Callable[[M], bool]) -> int:
        """時刻tでcondition(prod[l,j))が真であり続ける最大のjを返す"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        assert self._lower <= l <= self._upper, f"index out of range: l={l}"
        value = self._e
        j = l
        stack: list[tuple[PersistentSegmentTree.Node | None, int, int]] = [
            (self._roots[t], self._lower, self._upper)
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

    def min_left(self, t: int, r: int, condition: Callable[[M], bool]) -> int:
        """時刻tでcondition(prod[j,r))が真であり続ける最小のjを返す"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        assert self._lower <= r <= self._upper, f"index out of range: r={r}"
        value = self._e
        j = r
        stack: list[tuple[PersistentSegmentTree.Node | None, int, int]] = [
            (self._roots[t], self._lower, self._upper)
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

    def _update(self, node: "PersistentSegmentTree.Node") -> None:
        if node.left and node.right:
            node.value = self._op(node.left.value, node.right.value)
        elif node.left:
            node.value = node.left.value
        elif node.right:
            node.value = node.right.value
        else:
            node.value = self._e

    @property
    def latest_t(self) -> int:
        return len(self._roots) - 1
