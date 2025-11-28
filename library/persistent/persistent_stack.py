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
            self.parent = None

    def __init__(self) -> None:
        self._tail = None
        self._version = dict()
    
    def get(self) -> object:
        """末尾の要素を取得"""
        return self._tail.value
    
    def push(self, value: object) -> None:
        """追加"""
        new = PersistentStack.Node(value)
        new.parent = self._tail
        self._tail = new
    
    def pop(self) -> object:
        """末尾の要素を取り出す"""
        assert self._tail,"stack is empty"
        value = self._tail.value
        self._tail = self._tail.parent
        return value
    
    def save(self, key: object) -> None:
        """keyに今の状態を保存"""
        self._version[key] = self._tail
    
    def load(self, key: object) -> None:
        """stackをkeyの状態にする"""
        assert key in self._version,f"version {key} does not exist"
        self._tail = self._version[key]
    
    def is_empty(self) -> bool:
        """stackが空か"""
        return self._tail is None