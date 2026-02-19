from sortedcontainers import SortedSet

class IntervalSet:
    """
    区間を管理する[l, r)
    偶数番目が l, 奇数番目が r
    """
    def __init__(self) -> None:
        self._data = SortedSet()
        self._sum_length = 0
    
    def __iter__(self):
        it = iter(self._data)
        while True:
            try:
                l = next(it)
                r = next(it)
                yield (l, r)
            except StopIteration:
                return
    
    def contains(self, x: int) -> bool:
        """区間にxが含まれるか"""
        i = self._data.bisect_right(x)
        return i % 2
    
    def add(self, l: int, r: int) -> None:
        """区間[l, r)を追加"""
        i = self._data.bisect_left(l)
        i -= i % 2
        j = self._data.bisect_right(r)
        j += i % 2
        for _ in range(i, j, 2):
            tl = self._data.pop(i)
            tr = self._data.pop(i)
            self._sum_length -= tr - tl
            l = min(l, tl)
            r = max(r, tr)
        self._sum_length += r - l
        self._data.add(l)
        self._data.add(r)

    def discard(self, l: int, r: int) -> None:
        pass