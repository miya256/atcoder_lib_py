from bisect import bisect_left

class Compressor:
    """
    座標圧縮

    Methods:
        original(compressed): 圧縮後の値 -> 元の値
        compress(original)  : 元の値 -> 圧縮後の値
    """
    def __init__(self, numbers: set) -> None:
        self._numbers = sorted(set(numbers))
        self._compressed = {v: i for i, v in enumerate(self._numbers)}
    
    def __call__(self, original: int) -> int:
        return self.compress(original)
    
    def __repr__(self) -> str:
        return f"{self._compressed}"

    def original(self, compressed: int) -> int:
        """圧縮後の値から元の値を返す"""
        return self._numbers[compressed]

    def compress(self, original: int) -> int:
        """元の値から圧縮後の値を返す"""
        if original not in self._compressed:
            self._compressed[original] = bisect_left(self._numbers, original)
        return self._compressed[original]