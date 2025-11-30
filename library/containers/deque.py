class Deque:
    """
    ランダムアクセス可能 deque

    Methods:
        get(i)         : i番目を取得
        set(i, val)    : i番目に代入
        is_full()      : 満タンか
        is_empty()     : 空か
        appendleft(val): 左に追加
        append(val)    : 右に追加
        popleft()      : 左から取り出す
        pop()          : 右から取り出す
    """
    def __init__(self, data: list = []) -> None:
        self._buffer = data + [None] * (1<<20 - len(data))
        self._head = 0
        self._tail = len(data)
        self._cur = 0
    
    def __getitem__(self, i: int) -> object:
        """"i番目を取得"""
        return self.get(i)
    
    def __setitem__(self, i: int, val: object) -> None:
        """i番目をvalに"""
        self.set(i, val)
    
    def __len__(self) -> int:
        """dequeのサイズ"""
        return self._tail - self._head
    
    def __contains__(self, val: object) -> bool:
        """valがあるか"""
        return val in self._buffer
    
    def __iter__(self):
        self._cur = 0
        return self

    def __next__(self) -> object:
        if self._cur < len(self):
            val = self[self._cur]
            self._cur += 1
            return val
        raise StopIteration
    
    def __repr__(self):
        return f'Deque({list(self)})'
    
    def get(self, i: int) -> object:
        """"i番目を取得"""
        assert -len(self) <= i < len(self), f"index {i} out of range"
        return self._buffer[self._index(i)]
    
    def set(self, i: int, val: object) -> None:
        """i番目をvalに"""
        assert -len(self) <= i < len(self), f"index {i} out of range"
        self._buffer[self._index(i)] = val
    
    def is_full(self) -> bool:
        """すべて埋まっているか"""
        return len(self) == len(self._buffer)
    
    def is_empty(self) -> bool:
        """空か"""
        return len(self) == 0
    
    def appendleft(self, val: object) -> None:
        """左に追加"""
        if self.is_full():
            self._extend()
        self._head -= 1
        self._buffer[self._head % len(self._buffer)] = val
    
    def append(self, val: object) -> None:
        """右に追加"""
        if self.is_full():
            self._extend()
        self._buffer[self._tail % len(self._buffer)] = val
        self._tail += 1
    
    def popleft(self) -> object:
        """左の要素を取り出す"""
        assert not self.is_empty(), "deque is empty"
        val = self._buffer[self._head % len(self._buffer)]
        self._head += 1
        return val
    
    def pop(self) -> object:
        """右の要素を取り出す"""
        assert not self.is_empty(), "deque is empty"
        self._tail -= 1
        val = self._buffer[self._tail % len(self._buffer)]
        return val
    
    def _index(self, i: int) -> int:
        if i >= 0:
            return (self._head + i) % len(self._buffer)
        else:
            return (self._tail + i) % len(self._buffer)
    
    def _extend(self) -> None:
        head = self._head
        buflen = len(self._buffer)
        self._buffer = self._buffer[head % buflen:] + self._buffer[:head % buflen] + [None]*buflen
        self._head -= head
        self._tail -= head
        