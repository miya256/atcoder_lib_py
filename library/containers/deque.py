from typing import TypeVar, Generic, Iterator

T = TypeVar("T")


class Deque(Generic[T]):
    """
    ランダムアクセス可能 deque

    Methods:
        get(i)           : i番目を取得
        set(i, value)    : i番目に代入
        is_full()        : 満タンか
        is_empty()       : 空か
        appendleft(value): 左に追加
        append(value)    : 右に追加
        popleft()        : 左から取り出す
        pop()            : 右から取り出す
    """

    def __init__(self, data: list[T] | None = None) -> None:
        if data is None:
            data = []
        self._buffer: list[T] = data + [None] * (1 << 20 - len(data))  # type: ignore
        self._head: int = 0
        self._tail: int = len(data)

    def __getitem__(self, i: int) -> T:
        """ "i番目を取得"""
        return self.get(i)

    def __setitem__(self, i: int, value: T) -> None:
        """i番目をvalに"""
        self.set(i, value)

    def __len__(self) -> int:
        """dequeのサイズ"""
        return self._tail - self._head

    def __contains__(self, value: T) -> bool:
        """valがあるか"""
        return value in self._buffer

    def __iter__(self) -> Iterator[T]:
        for i in range(len(self)):
            yield self._buffer[self._index(i)]

    def __repr__(self) -> str:
        return f"Deque({list(self)})"

    def get(self, i: int) -> T:
        """ "i番目を取得"""
        orig_i = i
        i += len(self) if i < 0 else 0
        assert 0 <= i < len(self), f"index out of range: i={orig_i}->{i}"

        return self._buffer[self._index(i)]

    def set(self, i: int, value: T) -> None:
        """i番目をvalに"""
        orig_i = i
        i += len(self) if i < 0 else 0
        assert 0 <= i < len(self), f"index out of range: i={orig_i}->{i}"

        self._buffer[self._index(i)] = value

    def is_full(self) -> bool:
        """すべて埋まっているか"""
        return len(self) == len(self._buffer)

    def is_empty(self) -> bool:
        """空か"""
        return len(self) == 0

    def appendleft(self, value: T) -> None:
        """左に追加"""
        if self.is_full():
            self._extend()
        self._head -= 1
        self._buffer[self._head % len(self._buffer)] = value

    def append(self, value: T) -> None:
        """右に追加"""
        if self.is_full():
            self._extend()
        self._buffer[self._tail % len(self._buffer)] = value
        self._tail += 1

    def popleft(self) -> T:
        """左の要素を取り出す"""
        assert not self.is_empty(), "deque is empty"
        value = self._buffer[self._head % len(self._buffer)]
        self._head += 1
        return value

    def pop(self) -> T:
        """右の要素を取り出す"""
        assert not self.is_empty(), "deque is empty"
        self._tail -= 1
        value = self._buffer[self._tail % len(self._buffer)]
        return value

    def _index(self, i: int) -> int:
        return (self._head + i) % len(self._buffer)

    def _extend(self) -> None:
        head = self._head
        buflen = len(self._buffer)
        self._buffer = (
            self._buffer[head % buflen :]
            + self._buffer[: head % buflen]
            + [None] * buflen
        )  # type: ignore
        self._head -= head
        self._tail -= head
