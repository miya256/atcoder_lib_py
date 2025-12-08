from typing import Generic, TypeVar, Callable

T = TypeVar("T")

class FenwickTree(Generic[T]):
    """
    区間の積を O(log n) で計算

    Attributes:
        op    : 二項演算
        op_inv: opの逆演算
        e     : opの単位元

    Methods:\n
        get(i)         : i番目を取得
        set(i, x)      : i番目をxにする
        apply(i, x)      : i番目にxを作用
        prod(l, r)      : 区間[l, r)の総積
    """
    def __init__(
        self,
        op: Callable[[T, T], T],
        op_inv: Callable[[T, T], T],
        e: T, data: list|int
    ) -> None:
        if isinstance(data,int):
            data = [e for _ in range(data)]
        self._n = len(data)
        self._op = op
        self._op_inv = op_inv
        self._e = e
        self._data = data
        self._tree = [0] * (self._n + 1)
        self.all_prod = self._build(data)

    def _build(self, data: list) -> T:
        cun = [self._e for _ in range(self._n + 1)]
        for i in range(1, self._n+1):
            cun[i] = self._op(cun[i-1], data[i-1])
            self._tree[i] = self._op_inv(cun[i], cun[i-(-i&i)])
        return cun[-1]
    
    def __len__(self) -> int:
        """データの大きさ"""
        return self._n
    
    def __getitem__(self, i: int) -> T:
        """i番目を取得"""
        return self.get(i)
    
    def __setitem__(self, i: int, x: T) -> None:
        """i番目をxにする"""
        self.set(i, x)
    
    def __repr__(self) -> str:
        return f'FenwickTree {self._data}'
    
    def get(self, i: int) -> T:
        """i番目を取得"""
        assert 0 <= i < self._n, f"index error i={i}"
        return self._data[i]
    
    def apply(self, i: int, x: T) -> None:
        """i番目にxを作用。写像はop"""
        assert 0 <= i < self._n, f"index error i={i}"
        self._data[i] = self._op(self._data[i], x)
        self.all_prod = self._op(self.all_prod, x)
        i += 1
        while i <= self._n:
            self._tree[i] = self._op(self._tree[i], x)
            i += -i & i
    
    def set(self, i: int, x: T) -> None:
        """加えるではなく、更新"""
        assert 0 <= i < self._n, f"index error i={i}"
        self.apply(i, self._op_inv(x, self._data[i]))
    
    def _prod(self, i: int) -> T:
        """区間[0, i)の積"""
        prod = self._e
        while i > 0:
            prod = self._op(prod, self._tree[i])
            i -= -i & i
        return prod
    
    def prod(self, l: int, r: int) -> T:
        """区間[l,r)の総積"""
        assert 0 <= l <= r <= self._n, f"index error [l,r)=[{l},{r})"
        return self._op_inv(self._prod(r), self._prod(l))