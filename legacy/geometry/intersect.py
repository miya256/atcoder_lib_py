def intersection_point(p1, p2, q1, q2):
    """線分p1p2 と 線分q1q2 の共有点 tupleでもok"""
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    def sign(x):
        return 1 if x > 0 else -1 if x < 0 else 0
    def orientation(a, b, c):
        cross = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
        return sign(cross)
    def segments_intersect(p1, p2, q1, q2):
        if (max(p1.x, p2.x) < min(q1.x, q2.x) or
            max(q1.x, q2.x) < min(p1.x, p2.x) or
            max(p1.y, p2.y) < min(q1.y, q2.y) or
            max(q1.y, q2.y) < min(p1.y, p2.y)):
            return False
        o1 = orientation(p1, p2, q1)
        o2 = orientation(p1, p2, q2)
        o3 = orientation(q1, q2, p1)
        o4 = orientation(q1, q2, p2)
        return (o1 * o2 <= 0) and (o3 * o4 <= 0)
    
    if isinstance(p1, tuple): p1 = Point(*p1)
    if isinstance(p2, tuple): p2 = Point(*p2)
    if isinstance(q1, tuple): q1 = Point(*q1)
    if isinstance(q2, tuple): q2 = Point(*q2)
    
    #共有点がないなら
    if not segments_intersect(p1, p2, q1, q2):
        return None
    
    det = (p1.x - p2.x) * (q2.y - q1.y) - (q2.x - q1.x) * (p1.y - p2.y)
    t = ((q2.y - q1.y) * (q2.x - p2.x) + (q1.x - q2.x) * (q2.y - p2.y))
    x = (t * p1.x + (det - t) * p2.x) / det
    y = (t * p1.y + (det - t) * p2.y) / det
    return x, y