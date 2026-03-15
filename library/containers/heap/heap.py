from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class Heap(Generic[T]):
    """
    優先度付きキュー（ヒープ）

    Methods:
        add(value): 追加
        pop()     : 削除
    """

    def __init__(self, compare: Callable[[T, T], bool]) -> None:
        self._heap: list[T] = [None]  # type: ignore
        self._compare = compare

    def __len__(self) -> int:
        """長さ"""
        return len(self._heap) - 1

    def push(self, value: T) -> None:
        """valueを追加"""
        self._heap.append(value)
        self._sift_up(len(self))

    def pop(self) -> T:
        """0番目を取り出す"""
        assert len(self) > 0, "heap is empty"
        res = self._heap[1]
        self._heap[1] = self._heap[-1]
        self._heap.pop()
        self._sift_down(1)
        return res

    def _sift_up(self, i: int) -> None:
        while i > 1:
            if self._compare(self._heap[i // 2], self._heap[i]):
                break
            self._heap[i // 2], self._heap[i] = self._heap[i], self._heap[i // 2]
            i >>= 1

    def _sift_down(self, i: int) -> None:
        while True:
            smallest = i
            if i * 2 <= len(self) and self._compare(
                self._heap[i * 2], self._heap[smallest]
            ):
                smallest = i * 2
            if i * 2 + 1 <= len(self) and self._compare(
                self._heap[i * 2 + 1], self._heap[smallest]
            ):
                smallest = i * 2 + 1

            if smallest == i:
                break
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            i = smallest


def compare(parent, child) -> bool:
    """parent が child より優先されるなら True"""
    return parent < child
