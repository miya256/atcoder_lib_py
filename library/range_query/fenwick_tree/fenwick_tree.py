class FenwickTree:
    """
    区間の和を O(log n) で計算

    Methods:\n
        get(i)         : i番目を取得
        set(i, x)      : i番目をxにする
        add(i, x)      : i番目にxを加算
        sum(l, r)      : 区間[l, r)の和
        bisect_left(x) : 累積和配列とみなし、二分探索
        bisect_right(x): 累積和配列とみなし、二分探索
    """

    def __init__(self, data: list|int) -> None:
        if isinstance(data, int):
            data = [0 for _ in range(data)]
        self._n = len(data)
        self._data = data
        self._tree = [0] * (self._n + 1)
        self.all_sum = self._build(data)
    
    def _build(self, data: list) -> int:
        """treeを作成。すべての和を返す"""
        cum = [0] * (self._n + 1)
        for i in range(1, self._n+1):
            cum[i] = cum[i-1] + data[i-1]
            self._tree[i] = cum[i] - cum[i-(-i&i)]
        return cum[-1]
    
    def __len__(self) -> int:
        """データの大きさ"""
        return self._n
    
    def __getitem__(self, i: int) -> int:
        """i番目を取得"""
        return self.get(i)
    
    def __setitem__(self, i: int, x: int) -> None:
        """i番目をxにする"""
        self.set(i, x)
    
    def __repr__(self) -> str:
        return f'FenwickTree {self._data}'
    
    def get(self, i: int) -> int:
        """i番目を取得"""
        assert 0 <= i < self._n, f"index error i={i}"
        return self._data[i]
    
    def add(self, i: int, x: int) -> None:
        """i番目にxを加える"""
        assert 0 <= i < self._n, f"index error i={i}"
        self._data[i] += x
        self.all_sum += x
        i += 1
        while i <= self._n:
            self._tree[i] += x
            i += -i & i
    
    def set(self, i: int, x: int) -> None:
        """i番目をxにする"""
        assert 0 <= i < self._n, f"index error i={i}"
        self.add(i, x - self._data[i])
    
    def _sum(self, i: int) -> int:
        """区間[0, i)の和"""
        sum = 0
        while i > 0:
            sum += self._tree[i]
            i -= -i & i
        return sum
    
    def sum(self, l: int, r: int) -> int:
        """区間[l, r)の和"""
        assert 0 <= l <= r <= self._n, f"index error [l,r)=[{l},{r})"
        return self._sum(r) - self._sum(l)
    
    def bisect_left(self, x: int) -> int:
        """区間[0, index)の和がx以上になる最小のindex"""
        i = 1 << self._n.bit_length() - 1
        value = 0
        while not i & 1:
            if i-1 < self._n and value + self._tree[i] < x:
                value += self._tree[i]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (value + self._tree[i] < x)
    
    def bisect_right(self, x: int) -> int:
        """区間[0, index)の和がx超過になる最小のindex"""
        i = 1 << self._n.bit_length()-1
        value = 0
        while not i & 1:
            if i-1 < self._n and value + self._tree[i] <= x:
                value += self._tree[i]
                i += (-i & i) >> 1
            else:
                i -= (-i & i) >> 1
        return i-1 + (value + self._tree[i] <= x)