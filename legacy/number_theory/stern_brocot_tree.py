class SternBrocotTree:
    #p, q, r, s は、
    #区間 [p/q, r/s] や (p+r)/(q+s) という数字
    class Fraction:
        def __init__(self, p, q, r, s):
            self.data = (p, q, r, s)
        
        def __lt__(self, other):
            if isinstance(other, float) or isinstance(other, int):
                return float(self) < other
            p1, q1, r1, s1 = self.data
            p2, q2, r2, s2 = other.data
            return (p1 + r1) * (q2 + s2) < (p2 + r2) * (q1 + s1)
        
        def __gt__(self, other):
            if isinstance(other, float) or isinstance(other, int):
                return float(self) > other
            return other.__lt__(self)
        
        def __eq__(self, other):
            if isinstance(other, float) or isinstance(other, int):
                return abs(float(self) - other) < 1e-18
            p1, q1, r1, s1 = self.data
            p2, q2, r2, s2 = other.data
            return (p1 + r1) * (q2 + s2) == (p2 + r2) * (q1 + s1)

        def __float__(self):
            p, q, r, s = self.data
            return (p + r) / (q + s)
        
        def numerator(self):
            return self.data[0] + self.data[2]
        
        def denominator(self):
            return self.data[1] + self.data[3]
        
        def moved_left(self, d):
            p, q, r, s = self.data
            return SternBrocotTree.Fraction(p, q, d*p+r, d*q+s)
        
        def moved_right(self, d):
            p, q, r, s = self.data
            return SternBrocotTree.Fraction(p+d*r, q+d*s, r, s)
        
        def move_left(self, d):
            p, q, r, s = self.data
            self.data = (p, q, d*p+r, d*q+s)
        
        def move_right(self, d):
            p, q, r, s = self.data
            self.data = (p+d*r, q+d*s, r, s)
    
    def __init__(self):
        self.root = (0, 1, 1, 0)

    def _within(self, frac: Fraction, limit):
        p, q, r, s = frac.data
        return p + r <= limit and q + s <= limit
    
    def _max_left_steps(self, cur, target, limit):
        """何回左に行くか"""
        d = 1
        while self._within(cur.moved_left(d), limit) and cur.moved_left(d) > target:
            d <<= 1
        low, high = d//2, d
        while high - low > 1:
            mid = (low + high) // 2
            if self._within(cur.moved_left(mid), limit) and cur.moved_left(mid) > target:
                low = mid
            else:
                high = mid
        if self._within(cur.moved_left(high), limit):
            return high, False
        return high, True
    
    def _max_right_steps(self, cur, target, limit):
        d = 1
        while self._within(cur.moved_right(d), limit) and cur.moved_right(d) < target:
            d <<= 1
        low, high = d//2, d
        while high - low > 1:
            mid = (low + high) // 2
            if self._within(cur.moved_right(mid), limit) and cur.moved_right(mid) < target:
                low = mid
            else:
                high = mid
        if self._within(cur.moved_right(high), limit):
            return high, False
        return high, True

    def encode(self, target, limit=1<<61):
        """左へ行くなら1、右へ行くなら0"""
        rle_path = []
        cur = SternBrocotTree.Fraction(*self.root)
        reached = False
        while not reached:
            if cur > target:
                d, reached = self._max_left_steps(cur, target, limit)
                cur.move_left(d)
                rle_path.append((1, d))
            else:
                d, reached = self._max_right_steps(cur, target, limit)
                cur.move_right(d)
                rle_path.append((0, d))
        return rle_path
    
    def decode(self, rle_path) -> Fraction:
        """pathに対応する有理数"""
        cur = SternBrocotTree.Fraction(*self.root)
        for is_left, d in rle_path:
            if is_left:
                cur.move_left(d)
            else:
                cur.move_right(d)
        return cur
    
    def lca(self, frac1, frac2):
        """2つの有理数に対応する点のlcaの有理数"""
        path1 = self.encode(frac1)
        path2 = self.encode(frac2)
        cur = SternBrocotTree.Fraction(*self.root)
        for p1, p2 in zip(path1, path2):
            if p1 == p2:
                if p1[0]:
                    cur.move_left(p1[1])
                else:
                    cur.move_right(p1[1])
            else:
                if p1[0] != p2[0]:
                    return cur
                if p1[0]:
                    cur.move_left(min(p1[1], p2[1]))
                else:
                    cur.move_right(min(p1[1], p2[1]))
                return cur
    
    def ancestor(self, frac, depth):
        """fracの祖先で深さdepthである有理数"""
        path = self.encode(frac)
        cur = SternBrocotTree.Fraction(*self.root)
        for is_left, d in path:
            if d <= depth:
                if is_left:
                    cur.move_left(d)
                else:
                    cur.move_right(d)
                depth -= d
            else:
                if is_left:
                    cur.move_left(depth)
                else:
                    cur.move_right(depth)
                return cur
    
    def range(self, frac):
        """p/q ~ r/s"""
        p, q, r, s = self.decode(self.encode(frac)).data
        return p, q, r, s

R = float(input())
n = int(input())
sbt = SternBrocotTree()
frac = sbt.decode(sbt.encode(R, n))
p,q,r,s = frac.data
if R - p/q <= r/s - R:
    print(p, q)
else:
    print(r,s)