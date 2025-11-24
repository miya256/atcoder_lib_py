class FPS:
    def __init__(self, a: list | int) -> None:
        if isinstance(a, int):
            a = [1] + [0] * a
        self.a = a

    def __mul__(self, other):
        self.a = convolution(self.a, other.a)
        #みたいな
    
    def mul_(self, c, k):
        """1+cx^kをかける"""
        self.a[i] += c * self.a[i-k]
        #みたいな