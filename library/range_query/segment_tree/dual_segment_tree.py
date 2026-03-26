from typing import Generic, TypeVar, Callable, Iterator

M = TypeVar("MonoidElement")  # type: ignore
O = TypeVar("Operator")  # type: ignore

# 可換じゃないといけねえ


class DualSegmentTree(Generic[M]):
    def __init__(
        self,
        e: M,
        mapping: Callable[[O, M], M],
        composition: Callable[[O, O], O],
        id: O,
        data: list[M] | int,
    ) -> None:
        if isinstance(data, int):
            data = [e for _ in range(data)]
        self.n = len(data)
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id
        self._size = 1 << (len(data) - 1).bit_length()
        self._tree = [id for _ in range(self._size)] + [e for _ in range(self._size)]
        self._build(data)

    def _build(self, data: list[M]) -> None:
        for i, val in enumerate(data, start=self._size):
            self._tree[i] = val

    def get(self, i: int) -> M:
        i += self._size
        res = self._e
        while i:
            res = self._mapping(res, self._tree[i])
            i >>= 1
        return res

    def apply(self, l, r, f):
        l += self._size
        r += self._size
        while l < r:
            if l & 1:
                self._tree[l] = self._mapping(self._tree[l], f)
                l += 1
            if r & 1:
                r -= 1
                self._tree[r] = self._mapping(self._tree[r], f)
            l >>= 1
            r >>= 1

    def __str__(self):
        return f"DualSegmentTree {[self[i] for i in range(self.n)]}"
