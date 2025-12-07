from sortedcontainers import SortedSet
from collections import deque

class ConvexHullTrick:
    """
    Attributes:
        op        : max or min
        slope_type: 追加する直線の傾きの単調性
        query_type: クエリの単調性
        単調増加 -> 1, 単調減少 -> -1, ランダム -> 0
    
    Methods:
        add(m,b): 直線y=mx+bを追加
        query(x): xのときyの最大最小
    """
    class Line:
        # m,bはintってあるけど、fractionでもいいかも
        def __init__(self, m: int, b: int) -> None:
            self.m = m #傾き
            self.b = b #切片
        
        def __call__(self, x: int) -> int:
            return self.m * x + self.b
        
    def __init__(self, op, slope_type: int = 0, query_type: int = 0) -> None:
        self._op = op
        self._slope_type = slope_type
        self._query_type = query_type
        self._lines = SortedSet(key=lambda line: -line.m) if slope_type == 0 else deque()
    
    def add(self, m: int, b: int) -> None:
        """y=mx+bを追加"""
        line = self.Line(m,b)
        if self._slope_type == 0:
            self._add(line)
        if self._slope_type == 1:
            self._add_left(line)
        if self._slope_type == -1:
            self._add_right(line)
    
    def query(self, x: int) -> int:
        """xのとき、yの最大or最小"""
        if self._query_type == 0:
            return self._query(x)
        if self._query_type == 1:
            return self._query_from_left(x)
        if self._query_type == -1:
            return self._query_from_right(x)
    
    def _add(self, line: "ConvexHullTrick.Line") -> None:
        position = self._lines.bisect_left(line)
        #追加する直線が不要なら追加しない
        if 0 < position < len(self._lines) and self._is_bad(self._lines[position-1], line, self._lines[position]):
            return
        #右側の不要な直線を削除
        while position+1 < len(self._lines) and self._is_bad(line, self._lines[position], self._lines[position+1]):
            self._lines.pop(position)
        #左側の不要な直線を削除
        while position-2 >= 0 and self._is_bad(self._lines[position-2], self._lines[position-1], line):
            self._lines.pop(position-1)
            position -= 1
        self._lines.add(line)
    
    def _add_left(self, line: "ConvexHullTrick.Line") -> None:
        while len(self._lines) >= 2 and self._is_bad(line, self._lines[0], self._lines[1]):
            self._lines.popleft()
        self._lines.appendleft(line)
    
    def _add_right(self, line: "ConvexHullTrick.Line") -> None:
        while len(self._lines) >= 2 and self._is_bad(self._lines[-2], self._lines[-1], line):
            self._lines.pop()
        self._lines.append(line)
    
    def _query(self, x: int) -> int:
        l, r = 0, len(self._lines)
        while r-l > 1:
            mid = (l+r)//2
            if self._compare(self._lines[mid-1](x), self._lines[mid](x)):
                l = mid
            else:
                r = mid
        return self._lines[l](x)
    
    def _query_from_left(self, x: int) -> int:
        while len(self._lines) > 1 and self._compare(self._lines[0](x), self._lines[1](x)):
            self._lines.popleft()
        return self._lines[0](x)
    
    def _query_from_right(self, x: int) -> int:
        while len(self._lines) > 1 and self._compare(self._lines[-1](x), self._lines[-2](x)):
            self._lines.pop()
        return self._lines[-1](x)
    
    def _compare(self, a: int, b: int) -> bool:
        """op(a,b) == b(右辺のほうが良いか)"""
        if self._op == min: return a >= b
        if self._op == max: return a <= b
    
    def _is_bad(
            self,
            line1: "ConvexHullTrick.Line",
            line2: "ConvexHullTrick.Line",
            line3: "ConvexHullTrick.Line"
        ) -> bool:
        """line2が不要か"""
        left = (line3.b - line2.b) * (line2.m - line1.m)
        right = (line3.m - line2.m) * (line2.b - line1.b)
        return self._compare(left, right)