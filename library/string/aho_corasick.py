from collections import deque


class AhoCorasick:
    """
    文字列の位置を検索する
    線形時間
    """

    class Node:
        def __init__(self, id: int) -> None:
            self.id = id
            self.children: dict[str, AhoCorasick.Node] = {}
            self.ends: set[str] = set()
            self.fail: AhoCorasick.Node

    def __init__(self, *string_set: set | list | tuple | str):
        self._chars = self._extract_chars(string_set)
        self._root = AhoCorasick.Node(0)
        self._root.fail = self._root
        self._patterns: set[str] = set()
        self.nodes: list[AhoCorasick.Node] = [self._root]
        self._next_id = 1
        self._built = False

    def _extract_chars(self, string_set) -> set[str]:
        unique = set()
        stack = [string_set]
        while stack:
            values = stack.pop()
            if isinstance(values, str):
                unique.update(*values)
            else:
                stack.extend(values)
        return unique

    def add(self, string: str) -> None:
        """検索したい文字列を追加"""
        self._patterns.add(string)
        current = self._root
        for char in string:
            if char not in current.children:
                node = AhoCorasick.Node(self._next_id)
                current.children[char] = node
                self.nodes.append(node)
                self._next_id += 1
            current = current.children[char]
        current.ends.add(string)

    def build(self) -> None:
        self._built = True
        dq: deque[AhoCorasick.Node] = deque()

        for char in self._chars:
            if char not in self._root.children:
                self._root.children[char] = self._root
            else:
                ch = self._root.children[char]
                ch.fail = self._root
                dq.append(ch)

        while dq:
            cur = dq.popleft()
            cur.ends |= cur.fail.ends

            for char in self._chars:
                if char not in cur.children:
                    cur.children[char] = cur.fail.children[char]
                else:
                    ch = cur.children[char]
                    ch.fail = cur.fail.children[char]
                    dq.append(ch)

    def find_all(self, string: str) -> dict[str, list[int]]:
        """
        見つかった文字列のindex
        例 {'a': [0, 5], 'ba': [4], 'bbca': [], 'abbc': [0], 'cba': [3]}
        """
        assert self._built, "build() is not called"
        res = {pattern: [] for pattern in self._patterns}
        cur = self._root
        for i, char in enumerate(string):
            cur = cur.children[char]
            for pattern in cur.ends:
                res[pattern].append(i - len(pattern) + 1)
        return res
