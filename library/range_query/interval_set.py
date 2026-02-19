from sortedcontainers import SortedSet

class IntervalSet:
    """
    区間を管理する[l, r)
    偶数番目が l, 奇数番目が r

    Methods:
    """

    def __init__(self) -> None:
        self._data = SortedSet()
    
    def __iter__(self):
        it = iter(self._data)
        while True:
            try:
                l = next(it)
                r = next(it)
                yield (l, r)
            except StopIteration:
                return
            
    def __or__(self, other: "IntervalSet") -> "IntervalSet":
        new_set = IntervalSet()
        for l, r in self:
            new_set.add(l, r)
        for l, r in other:
            new_set.add(l, r)
        return new_set
    
    def __and__(self, other: "IntervalSet") -> "IntervalSet":
        new_set = IntervalSet()
        i = j = 0
        while i < len(self._data) and j < len(other._data):
            l1, r1 = self._data[i], self._data[i+1]
            l2, r2 = other._data[j], other._data[j+1]
            l = max(l1, l2)
            r = min(r1, r2)
            if l < r:
                new_set.add(l, r)
            # rが小さいほうを次へ進める。同じなら両方進める
            if r1 <= r2:
                i += 2
            if r1 >= r2:
                j += 2
        return new_set

    def __xor__(self, other: "IntervalSet") -> "IntervalSet":
        new_set = IntervalSet()
        for l, r in self:
            new_set.flip(l, r)
        for l, r in other:
            new_set.flip(l, r)
        return new_set
    
    def __sub__(self, other: "IntervalSet") -> "IntervalSet":
        new_set = IntervalSet()
        for l, r in self:
            new_set.add(l, r)
        for l, r in other:
            new_set.discard(l, r)
        return new_set
    
    def __ior__(self, other: "IntervalSet") -> "IntervalSet":
        for l, r in other:
            self.add(l, r)
        return self
    
    def __iand__(self, other: "IntervalSet") -> "IntervalSet":
        self._data = (self & other)._data
        return self
    
    def __ixor__(self, other: "IntervalSet") -> "IntervalSet":
        for l, r in other:
            self.flip(l, r)
        return self
    
    def __isub__(self, other: "IntervalSet") -> "IntervalSet":
        for l, r in other:
            self.discard(l, r)
        return self
    
    def __repr__(self) -> str:
        return f"{[(l, r) for l, r in self]}"
    
    def add(self, l: int, r: int) -> None:
        """区間[l, r)を追加"""
        assert l < r, f"Invalid interval: [l,r)=[{l},{r})"
        i = self._data.bisect_left(l)
        i -= i % 2
        j = self._data.bisect_right(r)
        j += j % 2
        for _ in range(i, j, 2):
            l = min(l, self._data.pop(i))
            r = max(r, self._data.pop(i))
        self._data.add(l)
        self._data.add(r)

    def discard(self, l: int, r: int) -> None:
        """区間[l, r)を追加"""
        assert l < r, f"Invalid interval: [l,r)=[{l},{r})"
        # 反転させてから追加
        self._data.add(min(l, self._data[0]) - 1)
        self._data.add(max(r, self._data[-1]) + 1)
        self.add(l, r)
        # 戻す
        self._data.pop(0)
        self._data.pop()
    
    def flip(self, l: int, r: int) -> None:
        """区間[l, r)を反転"""
        assert l < r, f"Invalid interval: [l,r)=[{l},{r})"
        self._data.discard(l) if l in self._data else self._data.add(l)
        self._data.discard(r) if r in self._data else self._data.add(r)
    
    def contains(self, x: int) -> bool:
        """区間にxが含まれるか"""
        i = self._data.bisect_right(x)
        return i % 2
    
    def get_interval(self, x: int) -> tuple[int, int] | None:
        """xを含む区間を返す"""
        i = self._data.bisect_right(x)
        if i % 2 == 0: # xは区間に含まれない
            return None
        return self._data[i-1], self._data[i]

    def mex(self, x: int) -> int:
        """x 以上で区間に含まれない最小の数"""
        i = self._data.bisect_right(x)
        return self._data[i] if i % 2 else x
    
    def sum(self, l: int, r: int) -> int:
        """[l, r)の中の区間の長さの合計"""
        # 高速に求められたらいいなあ
        return 0
