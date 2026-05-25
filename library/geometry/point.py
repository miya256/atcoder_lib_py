import math


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __lt__(self, other: "Point") -> bool:
        """偏角の比較（原点は一番小さいとみなす）"""
        if self.x == self.y == 0:
            return True
        if other.x == other.y == 0:
            return False
        if self.is_upper_half() != other.is_upper_half():
            return self.is_upper_half()
        return self.x * other.y - self.y * other.x > 0

    def __repr__(self) -> str:
        return f"P((x, y)=({self.x}, {self.y}), deg={self.deg})"

    def to_tuple(self) -> tuple[int, int]:
        """タプルにする"""
        return self.x, self.y

    def is_upper_half(self) -> bool:
        """上半分（y>0 または y=0 かつ x>0）か"""
        return self.y > 0 or (self.y == 0 and self.x > 0)

    def rad_from(self, center: tuple[int, int]) -> float:
        """centerから見た角度"""
        x, y = center
        return math.atan2(self.y - y, self.x - x)

    def deg_from(self, center: tuple[int, int]) -> float:
        """centerから見た角度(0~360)"""
        deg = math.degrees(self.rad_from(center))
        return (deg + 360) % 360

    @property
    def rad(self) -> float:
        """原点から見た角度"""
        return self.rad_from((0, 0))

    @property
    def deg(self) -> float:
        """原点から見た角度(0~360)"""
        return self.deg_from((0, 0))
