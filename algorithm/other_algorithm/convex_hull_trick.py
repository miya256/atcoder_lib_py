#追加する直線の傾きがランダム
from sortedcontainers import SortedSet

class CHT:
    def __init__(self,ismax,key):
        """
        ismax = 0 : 最小値
        ismax = 1 : 最大値
        key = 0 : 条件なし
        key = -1 : xが単調減少
        key = 1 : xが単調増加
        """
        self.lines = SortedSet(key = lambda x : -x[0])
        self.ismax = ismax
        self.key = key

    def f(self, line, x):
        return line[0] * x + line[1]

    def need(self, line1, line2, line3):
        """line2が必要か"""
        if self.ismax:
            return (line3[1] - line2[1]) * (line2[0] - line1[0]) > (line2[1] - line1[1]) * (line3[0] - line2[0])
        else:
            return (line3[1] - line2[1]) * (line2[0] - line1[0]) < (line2[1] - line1[1]) * (line3[0] - line2[0])

    def add(self,a,b):
        """y=ax+bを追加"""
        line = (a,b)
        idx = self.lines.bisect_right(line)

        #追加する直線が不要なら追加しない
        if 0 < idx < len(self.lines) and not self.need(self.lines[idx-1], line, self.lines[idx]):
            return
        #右側の不要な直線を削除
        while idx+1 < len(self.lines) and not self.need(line, self.lines[idx], self.lines[idx+1]):
            self.lines.pop(idx)
        #左側の不要な直線を削除
        while idx-2 >= 0 and not self.need(self.lines[idx-2], self.lines[idx-1], line):
            self.lines.pop(idx-1)
            idx -= 1

        self.lines.add(line)

    def get(self, x):
        if self.ismax:
            if self.key == 1:
                while self.f(self.lines[0],x) < self.f(self.lines[1],x):
                    self.lines.pop(0)
                return self.f(self.lines[0],x)
            if self.key == -1:
                while self.f(self.lines[-1],x) < self.f(self.lines[-2],x):
                    self.lines.pop()
                return self.f(self.lines[-1],x)
            l,r = 0,len(self.lines)-1
            while r-l > 1:
                mid = (l+r)//2
                if self.f(self.lines[mid], x) > self.f(self.lines[mid+1], x):
                    r = mid
                else:
                    l = mid
            return max(self.f(self.lines[l],x),self.f(self.lines[r],x))
        else:
            if self.key == 1:
                while self.f(self.lines[0],x) > self.f(self.lines[1],x):
                    self.lines.pop(0)
                return self.f(self.lines[0],x)
            if self.key == -1:
                while self.f(self.lines[-1],x) > self.f(self.lines[-2],x):
                    self.lines.pop()
                return self.f(self.lines[-1],x)
            l,r = 0,len(self.lines)-1
            while r-l > 1:
                mid = (l+r)//2
                if self.f(self.lines[mid], x) < self.f(self.lines[mid+1], x):
                    r = mid
                else:
                    l = mid
            return min(self.f(self.lines[l],x),self.f(self.lines[r],x))


#追加する直線の傾きが単調
#今のところは、クエリも単調じゃないと使えない
#logがつく程度だから、どんな場合でも上のやつを使ったほうがいいかも
from collections import deque

class CHT:
    def __init__(self,ismax,key):
        """
        ismax = 0 : 最小値
        ismax = 1 : 最大値
        key = 0 : 条件なし
        key = -1 : xが単調減少
        key = 1 : xが単調増加
        """
        self.lines = deque()
        self.ismax = ismax
        self.key = key

    def f(self, line, x):
        return line[0] * x + line[1]

    def need(self, line1, line2, line3):
        """line2が必要か"""
        if self.ismax:
            return (line3[1] - line2[1]) * (line2[0] - line1[0]) > (line2[1] - line1[1]) * (line3[0] - line2[0])
        else:
            return (line3[1] - line2[1]) * (line2[0] - line1[0]) < (line2[1] - line1[1]) * (line3[0] - line2[0])
        
    def add(self,a,b):
        """y=ax+bを追加"""
        line = (a,b)
        if not self.lines or a < self.lines[0][0]:
            while len(self.lines) >= 2 and not self.need(self.lines[-2],self.lines[-1],line):
                self.lines.pop()
            self.lines.append(line)
        else:
            while len(self.lines) >= 2 and not self.need(line,self.lines[0],self.lines[1]):
                self.lines.popleft()
            self.lines.appendleft(line)

    def get(self, x):
        if self.ismax:
            if self.key == 1:
                while self.f(self.lines[0],x) < self.f(self.lines[1],x):
                    self.lines.popleft()
                return self.f(self.lines[0],x)
            if self.key == -1:
                while self.f(self.lines[-1],x) < self.f(self.lines[-2],x):
                    self.lines.pop()
                return self.f(self.lines[-1],x)
            l,r = 0,len(self.lines)-1
            while r-l > 1:
                mid = (l+r)//2
                if self.f(self.lines[mid], x) > self.f(self.lines[mid+1], x):
                    r = mid
                else:
                    l = mid
            return max(self.f(self.lines[l],x),self.f(self.lines[r],x))
        else:
            if self.key == 1:
                while self.f(self.lines[0],x) > self.f(self.lines[1],x):
                    self.lines.popleft()
                return self.f(self.lines[0],x)
            if self.key == -1:
                while self.f(self.lines[-1],x) > self.f(self.lines[-2],x):
                    self.lines.pop()
                return self.f(self.lines[-1],x)
            l,r = 0,len(self.lines)-1
            while r-l > 1:
                mid = (l+r)//2
                if self.f(self.lines[mid], x) < self.f(self.lines[mid+1], x):
                    r = mid
                else:
                    l = mid
            return min(self.f(self.lines[l],x),self.f(self.lines[r],x))

