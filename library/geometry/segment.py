class Segment:
    """線分"""
    def __init__(self, p: Point, q: Point) -> None:
        self.p = p
        self.q = q

    def intersects(self, other) -> bool:
        """共有点があるか"""
        def sign(x):
            return 1 if x > 0 else -1 if x < 0 else 0
        def orientation(a: Point, b: Point, c: Point) -> int:
            """点a,b,cが時計回りか反時計回りか直線か"""
            cross = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
            return sign(cross)
        
        if (max(self.p.x, self.q.x) < min(other.p.x, other.q.x) or
            max(other.p.x, other.q.x) < min(self.p.x, self.q.x) or
            max(self.p.y, self.q.y) < min(other.p.y, other.q.y) or
            max(other.p.y, other.q.y) < min(self.p.y, self.q.y)):
            return False
        o1 = orientation(self.p, self.q, other.p)
        o2 = orientation(self.p, self.q, other.q)
        o3 = orientation(other.p, other.q, self.p)
        o4 = orientation(other.p, other.q, self.q)
        return (o1 * o2 <= 0) and (o3 * o4 <= 0)