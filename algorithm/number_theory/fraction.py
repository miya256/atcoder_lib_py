class Fraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator #分子
        self.denominator = denominator #分母
        self._build()
    
    def _build(self):
        """約分、符号は分子に"""
        g = self._gcd(self.numerator, self.denominator)
        self.numerator //= g
        self.denominator //= g

        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
    
    @staticmethod
    def _gcd(n, m):
        while m:
            n, m = m, n % m
        return n
    
    @staticmethod
    def to_fraction(value):
        if isinstance(value, int):
            return Fraction(value, 1)
        return value
    
    def __eq__(self, other):
        """等しいか"""
        other = self.to_fraction(other)
        return self.numerator == other.numerator and self.denominator == other.denominator
    
    def __lt__(self, other):
        """<"""
        other = self.to_fraction(other)
        return self.numerator * other.denominator < self.denominator * other.numerator
    
    def __gt__(self, other):
        """>"""
        other = self.to_fraction(other)
        return self.numerator * other.denominator > self.denominator * other.numerator
    
    def __le__(self, other):
        """<="""
        other = self.to_fraction(other)
        return self.numerator * other.denominator <= self.denominator * other.numerator
    
    def __ge__(self, other):
        """>="""
        other = self.to_fraction(other)
        return self.numerator * other.denominator >= self.denominator * other.numerator
    
    #演算の左側の項がFractionの場合に呼ばれる
    def __add__(self, other):
        other = self.to_fraction(other)
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)
    
    def __sub__(self, other):
        other = self.to_fraction(other)
        numerator = self.numerator * other.denominator - other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)
    
    def __mul__(self, other):
        other = self.to_fraction(other)
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)
    
    def __truediv__(self, other):
        """/ ( // ではない )"""
        other = self.to_fraction(other)
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)
    
    #演算の右側の項がFractionの場合に呼ばれる
    def __radd__(self, other):
        return Fraction(other, 1) + self
    
    def __rsub__(self, other):
        return Fraction(other, 1) - self
    
    def __rmul__(self, other):
        return Fraction(other, 1) * self
    
    def __rtruediv__(self, other):
        """/ ( // ではない )"""
        return Fraction(other, 1) / self
    
    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)
    
    def __abs__(self):
        return Fraction(abs(self.numerator), self.denominator)
    
    def __int__(self):
        return self.numerator // self.denominator
    
    def __float__(self):
        return self.numerator / self.denominator
    
    def __hash__(self):
        return hash((self.numerator, self.denominator))
    
    def __str__(self):
        return f'{self.numerator}/{self.denominator}'