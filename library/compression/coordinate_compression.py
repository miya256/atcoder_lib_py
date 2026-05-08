from bisect import bisect_left


class CoordinateCompressor:
    """
    座標圧縮

    Methods:
        original(compressed): 圧縮後の値 -> 元の値
        compress(original)  : 元の値 -> 圧縮後の値
    """

    def __init__(self, *values: set | list | tuple | int) -> None:
        self._unique = self._build(values)
        self._compressed = {original: idx for idx, original in enumerate(self._unique)}

    def _build(self, values) -> list[int]:
        unique = set()
        stack = [values]
        while stack:
            values = stack.pop()
            if isinstance(values, int):
                unique.add(values)
            else:
                stack.extend(values)
        return sorted(unique)

    def __len__(self) -> int:
        return len(self._unique)

    def __call__(self, original: int) -> int:
        return self.compress(original)

    def __repr__(self) -> str:
        return f"Compressor({list(self._compressed.keys())})"

    def original(self, compressed: int) -> int:
        """圧縮後の値から元の値を返す"""
        return self._unique[compressed]

    def compress(self, original: int) -> int:
        """元の値から圧縮後の値を返す"""
        if original not in self._compressed:
            self._compressed[original] = bisect_left(self._unique, original)
        return self._compressed[original]
