from sortedcontainers import SortedSet
from collections import deque

class ConvexHullTrick:
    class Line:
        def __init__(self,m,b):
            self.m = m #傾き
            self.b = b #切片
        
        def __call__(self,x):
            return self.m * x + self.b
        
    def __init__(self,op,slope_type=0,query_type=0):
        """
        op: max or min
        slope_type: 追加する直線の傾きの単調性
        query_type: クエリの単調性
        単調増加 -> 1, 単調減少 -> -1, ランダム -> 0
        """
        self.op = op
        self.slope_type = slope_type
        self.query_type = query_type
        self.lines = SortedSet(key=lambda line:-line.m) if slope_type == 0 else deque()
    
    def _compare(self,a,b):
        """op(a,b) == b(右辺のほうが良いか)"""
        if self.op == min: return a >= b
        if self.op == max: return a <= b
    
    def isbad(self,line1,line2,line3):
        """line2が不要か"""
        left = (line3.b - line2.b) * (line2.m - line1.m)
        right = (line3.m - line2.m) * (line2.b - line1.b)
        return self._compare(left,right)
    
    def _add(self,line):
        position = self.lines.bisect_left(line)
        #追加する直線が不要なら追加しない
        if 0 < position < len(self.lines) and self.isbad(self.lines[position-1], line, self.lines[position]):
            return
        #右側の不要な直線を削除
        while position+1 < len(self.lines) and self.isbad(line, self.lines[position], self.lines[position+1]):
            self.lines.pop(position)
        #左側の不要な直線を削除
        while position-2 >= 0 and self.isbad(self.lines[position-2], self.lines[position-1], line):
            self.lines.pop(position-1)
            position -= 1
        self.lines.add(line)
    
    def _add_left(self,line):
        while len(self.lines) >= 2 and self.isbad(line,self.lines[0],self.lines[1]):
            self.lines.popleft()
        self.lines.appendleft(line)
    
    def _add_right(self,line):
        while len(self.lines) >= 2 and self.isbad(self.lines[-2],self.lines[-1],line):
            self.lines.pop()
        self.lines.append(line)
    
    def _query(self,x):
        l,r = 0,len(self.lines)
        while r-l > 1:
            mid = (l+r)//2
            if self._compare(self.lines[mid-1](x),self.lines[mid](x)):
                l = mid
            else:
                r = mid
        return self.lines[l](x)
    
    def _query_from_left(self,x):
        while len(self.lines) > 1 and self._compare(self.lines[0](x),self.lines[1](x)):
            self.lines.popleft()
        return self.lines[0](x)
    
    def _query_from_right(self,x):
        while len(self.lines) > 1 and self._compare(self.lines[-1](x),self.lines[-2](x)):
            self.lines.pop()
        return self.lines[-1](x)
    
    def add(self,m,b):
        """y=mx+bを追加"""
        line = self.Line(m,b)
        if self.slope_type == 0:
            self._add(line)
        if self.slope_type == 1:
            self._add_left(line)
        if self.slope_type == -1:
            self._add_right(line)
    
    def query(self,x):
        if self.query_type == 0:
            return self._query(x)
        if self.query_type == 1:
            return self._query_from_left(x)
        if self.query_type == -1:
            return self._query_from_right(x)