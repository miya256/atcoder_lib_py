class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __lt__(self, other) -> bool:
        """偏角の比較"""
        assert not (self.x == self.y == 0), "原点は比較できません"
        assert not (other.x == other.y == 0), "原点は比較できません"
        if self.is_upper_half() != other.is_upper_half():
            return self.is_upper_half()
        return self.x * other.y - self.y * other.x > 0
    
    def __repr__(self) -> str:
        return f"P({self.x}, {self.y})"
    
    def is_upper_half(self) -> bool:
        """上半分（y>0 または y=0 かつ x>0）か"""
        return self.y > 0 or (self.y == 0 and self.x > 0)