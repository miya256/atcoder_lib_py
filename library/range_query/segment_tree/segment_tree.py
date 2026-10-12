from typing import Generic, TypeVar, Callable, Iterator

M = TypeVar("MonoidElement")  # type: ignore


class SegmentTree(Generic[M]):
    """
    一点更新、区間取得を O(log n) で計算

    Attributes:
        op(x, y): xとyの二項演算（関数型）
        e       : opの単位元

    Methods:
        get(i)    : i番目を取得
        set(i, x) : i番目をxにする
        prod(l, r): 区間[l, r)の積
        all_prod(): 全体の積
        max_right(l, condition): condition(prod[l,j))が真になる最大のjを返す
        min_left(r, condition) : condition(prod[j,r))が真になる最小のjを返す
    """

    def __init__(
        self,
        op: Callable[[M, M], M],
        e: M,
        data: list[M] | int,
    ) -> None:
        if isinstance(data, int):
            data = [e for _ in range(data)]
        self._n = len(data)
        self._op = op
        self._e = e
        self._size = 1 << (len(data) - 1).bit_length()  # 最下段の長さ
        self._tree = [e for _ in range(self._size * 2)]
        self._build(data)

    def _build(self, data: list[M]) -> None:
        for i, val in enumerate(data):
            self._tree[i + self._size] = val
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def __len__(self) -> int:
        return self._n

    def __getitem__(self, i: int) -> M:
        """i番目を取得"""
        return self.get(i)

    def __setitem__(self, i: int, x: M) -> None:
        """i番目にxを代入"""
        self.set(i, x)

    def __iter__(self) -> Iterator[M]:
        for i in range(self._n):
            yield self.get(i)

    def __repr__(self) -> str:
        return f"SegmentTree {list(self)}"

    def __str__(self) -> str:
        return " ".join(map(str, list(self)))

    def get(self, i: int) -> M:
        """i番目を取得"""
        orig_i = i
        i += self._n if i < 0 else 0
        assert 0 <= i < self._n, f"index out of range: i={orig_i}->{i}"

        return self._tree[i + self._size]

    def set(self, i: int, x: M) -> None:
        """i番目にxを代入"""
        orig_i = i
        i += self._n if i < 0 else 0
        assert 0 <= i < self._n, f"index out of range: i={orig_i}->{i}"

        i += self._size
        self._tree[i] = x
        while i:
            i >>= 1
            self._update(i)

    def prod(self, l: int, r: int) -> M:
        """区間[l, r)の積"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )

        lt, rt = self._e, self._e
        l += self._size
        r += self._size
        while l < r:
            if l & 1:  # 右側だけなら
                lt = self._op(lt, self._tree[l])
                l += 1  # 上は範囲外も含むから一つ右にずらす
            if r & 1:  # 左側だけなら
                r -= 1
                rt = self._op(self._tree[r], rt)
            l >>= 1
            r >>= 1
        return self._op(lt, rt)

    def all_prod(self) -> M:
        """全体の積"""
        return self._tree[1]

    def max_right(self, l: int, condition: Callable[[M], bool]) -> int:
        """condition(prod[l,j))が真になる最大のjを返す"""
        orig_l = l
        l += self._n if l < 0 else 0
        assert 0 <= l <= self._n, f"index out of range: l={orig_l}->{l}"
        assert condition(self._e)

        if l == self._n:
            return self._n

        l += self._size
        value = self._e

        first = True
        while first or (l & -l) != l:
            first = False
            while l % 2 == 0:
                l >>= 1
            if not condition(self._op(value, self._tree[l])):
                while l < self._size:
                    l *= 2
                    if condition(self._op(value, self._tree[l])):
                        value = self._op(value, self._tree[l])
                        l += 1
                return l - self._size
            value = self._op(value, self._tree[l])
            l += 1

        return self._n

    def min_left(self, r: int, condition: Callable[[M], bool]) -> int:
        """condition(prod[j,r))が真になる最小のjを返す"""
        orig_r = r
        r += self._n if r < 0 else 0
        assert 0 <= r <= self._n, f"index out of range: r={orig_r}->{r}"
        assert condition(self._e)

        if r == 0:
            return 0

        r += self._size
        value = self._e

        first = True
        while first or (r & -r) != r:
            first = False
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not condition(self._op(self._tree[r], value)):
                while r < self._size:
                    r = 2 * r + 1
                    if condition(self._op(self._tree[r], value)):
                        value = self._op(self._tree[r], value)
                        r -= 1
                return r + 1 - self._size
            value = self._op(self._tree[r], value)

        return 0

    def _update(self, i: int) -> None:
        self._tree[i] = self._op(self._tree[2 * i], self._tree[2 * i + 1])
