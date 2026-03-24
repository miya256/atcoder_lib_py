from library.geometry.point import Point


def dist2(p: Point, q: Point) -> int:
    """二乗ユークリッド距離"""
    dx = p.x - q.x
    dy = p.y - q.y
    return dx * dx + dy * dy


def manhattan(p: Point, q: Point) -> int:
    """マンハッタン距離"""
    dx = p.x - q.x
    dy = p.y - q.y
    return abs(dx) + abs(dy)
