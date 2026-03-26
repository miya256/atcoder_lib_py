from typing import Iterator


class DualFenwickTree:
    """
    区間加算・一点取得を O(log n) で計算

    Methods:
        get(i)            : i番目を取得
        add(l, r, f)         : 区間[l, r)にfを加算
    """

    def __init__(self, data: list | int) -> None:
        if isinstance(data, int):
            data = [0 for _ in range(data)]
        self._n = len(data)
        self._tree = [0] * (self._n + 1)
        self._build(data)

    def _build(self, data) -> None:
        for i in range(self._n, 0, -1):
            self._tree[i] = data[i - 1]
            if i + (i & -i) <= self._n:
                self._tree[i] -= data[i - 1 + (i & -i)]

    def __len__(self) -> int:
        """データの大きさ"""
        return self._n

    def __getitem__(self, i: int) -> int:
        """i番目を取得"""
        return self.get(i)

    def __iter__(self) -> Iterator[int]:
        for i in range(self._n):
            yield self.get(i)

    def __repr__(self) -> str:
        return f"DualFenwickTree {list(self)}"

    def __str__(self) -> str:
        return " ".join(map(str, list(self)))

    def get(self, i: int) -> int:
        """i番目を取得"""
        orig_i = i
        i += self._n if i < 0 else 0
        assert 0 <= i < self._n, f"index out of range: i={orig_i}->{i}"

        sum = 0
        i += 1
        while i <= self._n:
            sum += self._tree[i]
            i += -i & i
        return sum

    def _add(self, i: int, f: int) -> None:
        """区間[0, i)にfを加算"""
        while i > 0:
            self._tree[i] += f
            i -= -i & i

    def add(self, l: int, r: int, f: int) -> None:
        """区間[l, r)にfを加算"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        self._add(l, -f)
        self._add(r, f)
