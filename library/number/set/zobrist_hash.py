import random


class ZobristHash:
    """
    集合のハッシュ
    hashのxorとかsumとかが等しければ同じ集合
    多重集合の場合はsumがいい
    """
    Mod = (1 << 61) - 1
    def __init__(self, elements: set) -> None:
        """numに含まれる要素のハッシュ値を生成"""
        self._hash = {
            element: hash for element, hash in zip(
                elements,
                random.sample(range(1, ZobristHash.Mod), len(elements))
            )
        }
    
    def __getitem__(self, element: object) -> int:
        return self.get_hash(element)
    
    def __setitem__(self, element: object, hash: int) -> None:
        self.set_hash(element, hash)
    
    def get_hash(self, element: object) -> int:
        """element のハッシュ値"""
        return self._hash[element]
    
    def set_hash(self, element: object, hash: int) -> None:
        """
        element のハッシュ値を hash にする
        0のハッシュ値を0にするときとかに使う
        """
        self._hash[element] = hash