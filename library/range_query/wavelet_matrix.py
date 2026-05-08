from typing import Literal


class WaveletMatrix:
    """
    Methods:
        --- O(log m) ---
        access(i)                  : i番目を取得
        rank(l,r,x)                : 区間[l,r)におけるxの出現回数
        select(x,k)                : k個目のxのindex
        kth_smallest(l,r,k)        : 区間[l,r)でk番目に小さい値
        kth_largest(l,r,k)         : 区間[l,r)でk番目に大きい値
        range_freq(l,r,lower,upper): 区間[l,r)でlower以上upper未満の個数
        prev_value(l,r,x)          : 区間[l,r)のうち、x未満の最大値
        next_value(l,r,x)          : 区間[l,r)のうち、x以上の最小値
    """

    class BitVector:
        def __init__(self, b: list[Literal[0, 1]]) -> None:
            self._pref = [0] + b
            for i in range(len(b)):
                self._pref[i + 1] += self._pref[i]

        def __getitem__(self, i: int) -> int:
            return self._pref[i + 1] - self._pref[i]

        def rank(self, bit: Literal[0, 1], i: int) -> int:
            """区間[0,i)のbitの個数"""
            return self._pref[i] if bit else i - self._pref[i]

        def select(self, bit: Literal[0, 1], k: int) -> int:
            """k番目のbitのindex"""
            l, r = 0, len(self._pref)
            while r - l > 1:
                mid = (l + r) // 2
                if self.rank(bit, mid) < k:
                    l = mid
                else:
                    r = mid
            return l

    def __init__(self, a: list[int], max_: int | None = None) -> None:
        self._n = len(a)
        self._max = max(a) if max_ is None else max_
        self.bit_size = self._max.bit_length()
        self._matrix = self._build(a)

    def _build(self, a: list[int]) -> list[BitVector]:
        matrix = []
        for d in range(self.bit_size)[::-1]:
            matrix.append(WaveletMatrix.BitVector([v >> d & 1 for v in a]))  # type: ignore
            zeros = [v for v in a if not v >> d & 1]
            ones = [v for v in a if v >> d & 1]
            a = zeros + ones
        return matrix

    def access(self, i: int) -> int:
        """i番目の値を取得"""
        orig_i = i
        i += self._n if i < 0 else 0
        assert 0 <= i < self._n, f"index out of range: i={orig_i}->{i}"

        value = 0
        for b, d in zip(self._matrix, range(self.bit_size)[::-1]):
            if b[i]:
                value |= 1 << d
                i = b.rank(0, self._n) + b.rank(1, i)
            else:
                i = b.rank(0, i)
        return value

    def rank(self, l: int, r: int, x: int) -> int:
        """区間[l,r)におけるxの出現回数"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        assert 0 <= x <= self._max, f"x={x} must be between 0 and {self._max}"

        for b, d in zip(self._matrix, range(self.bit_size)[::-1]):
            l, r = self._next_range(b, x >> d & 1, l, r)
        return r - l

    def select(self, x: int, k: int) -> int:
        """k個目のxのindex"""
        assert 0 <= x <= self._max, f"x={x} must be between 0 and {self._max}"
        assert k >= 1, f"invalid value: k={k}"
        l, r = 0, self._n
        for b, d in zip(self._matrix, range(self.bit_size)[::-1]):
            l, r = self._next_range(b, x >> d & 1, l, r)

        i = l + k - 1

        for b, d in zip(self._matrix[::-1], range(self.bit_size)):
            if x >> d & 1:
                i = b.select(1, i - b.rank(0, self._n) + 1)
            else:
                i = b.select(0, i + 1)

        if i < self._n:
            return i
        raise Exception(f"the number of {x} is less than or equal to {k}")

    def kth_smallest(self, l: int, r: int, k: int) -> int:
        """区間[l,r)でk番目に小さい値"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        assert 1 <= k <= r - l, f"invalid value: k={k}"

        value = 0
        for b, d in zip(self._matrix, range(self.bit_size)[::-1]):
            cnt0 = b.rank(0, r) - b.rank(0, l)
            bit = cnt0 < k
            value |= bit << d
            l, r = self._next_range(b, bit, l, r)
            if bit:
                k -= cnt0
        return value

    def kth_largest(self, l: int, r: int, k: int) -> int:
        """区間[l,r)でk番目に大きい値"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        assert 1 <= k <= r - l, f"invalid value: k={k}"

        value = 0
        for b, d in zip(self._matrix, range(self.bit_size)[::-1]):
            cnt1 = b.rank(1, r) - b.rank(1, l)
            bit = cnt1 >= k
            value |= bit << d
            l, r = self._next_range(b, bit, l, r)
            if not bit:
                k -= cnt1
        return value

    def range_freq(self, l: int, r: int, lower: int, upper: int) -> int:
        """区間[l,r)でlower以上upper未満の個数"""

        def _range_freq(l: int, r: int, upper: int) -> int:
            cnt = 0
            for b, d in zip(self._matrix, range(self.bit_size)[::-1]):
                bit = upper >> d & 1
                if bit:
                    cnt += b.rank(0, r) - b.rank(0, l)
                l, r = self._next_range(b, bit, l, r)
            return cnt

        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        assert 0 <= lower <= upper <= self._max, (
            f"lower={lower} and upper={upper} must be between 0 and {self._max}"
        )

        return _range_freq(l, r, upper) - _range_freq(l, r, lower)

    def prev_value(self, l: int, r: int, x: int) -> int | None:
        """区間[l,r)のうち、x未満の最大値"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        assert 0 <= x <= self._max, f"x={x} must be between 0 and {self._max}"

        cnt = self.range_freq(l, r, 0, x)
        return self.kth_smallest(l, r, cnt) if cnt > 0 else None

    def next_value(self, l: int, r: int, x: int) -> int | None:
        """区間[l,r)のうち、x以上の最小値"""
        orig_l = l
        orig_r = r
        l += self._n if l < 0 else 0
        r += self._n if r < 0 else 0
        assert 0 <= l <= r <= self._n, (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )
        assert 0 <= x <= self._max, f"x={x} must be between 0 and {self._max}"

        cnt = self.range_freq(l, r, x, self._max)
        return self.kth_largest(l, r, cnt) if cnt > 0 else None

    def _next_range(self, b: BitVector, bit: int, l: int, r: int) -> tuple[int, int]:
        """bの区間[l,r)において、bitであるものが次にどの区間にはいるか"""
        if bit:
            return b.rank(0, self._n) + b.rank(1, l), b.rank(0, self._n) + b.rank(1, r)
        return b.rank(0, l), b.rank(0, r)
