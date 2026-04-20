class PersistentStack:
    """
    永続スタック

    Methods:
        get     : 末尾を取得
        push    : 要素を追加
        pop     : 末尾を取り出す
        save    : 状態を保存
        load    : 状態をkeyに
        is_empty: 空か
    """

    class Node:
        def __init__(self, value: object) -> None:
            self.value = value
            self.parent: PersistentStack.Node | None = None

    def __init__(self) -> None:
        self._tails: list[PersistentStack.Node | None] = [None]

    def get(self, t: int) -> object:
        """時刻tの末尾の要素を取得"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        tail = self._tails[t]
        assert tail is not None, f"stack is empty: t={t}"
        return tail.value

    def push(self, t: int, value: object) -> int:
        """時刻tの末尾に追加"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        new = PersistentStack.Node(value)
        new.parent = self._tails[t]
        self._tails.append(new)
        return self.latest_t

    def pop(self, t: int) -> int:
        """末尾の要素を取り出す"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        tail = self._tails[t]
        assert tail is not None, f"stack is empty: t={t}"
        self._tails.append(tail.parent)
        return self.latest_t

    def is_empty(self, t: int) -> bool:
        """stackが空か"""
        assert 0 <= t <= self.latest_t, f"invalid time: t={t}, latest_t={self.latest_t}"
        return self._tails[t] is None

    @property
    def latest_t(self) -> int:
        return len(self._tails) - 1
