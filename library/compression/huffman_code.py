from collections import Counter
from heapq import heapify, heappush, heappop


class HuffmanCode:
    """
    ハフマン符号
    アルファベット小文字

    Methods:
        get_code: アルファベットの符号を返す
        get_char: 符号をアルファベットに復元
    """
    class Node:
        def __init__(self, cnt: int, char: str | None = None) -> None:
            self.cnt = cnt
            self.char = char  # 葉のみ文字を保持
            self.left = None
            self.right = None

    def __init__(self, string: str) -> None:
        self._root = self._make_tree(string.lower())
        self._code = {}
        self._build_code(self._root, "")

    def _make_tree(self, string: str) -> "HuffmanCode.Node":
        counter = Counter(c for c in string if c.islower())
        hq = [(cnt, id(node := HuffmanCode.Node(cnt, char)), node) for char, cnt in counter.items()]
        heapify(hq)

        while len(hq) > 1:
            cnt1, _, node1 = heappop(hq)
            cnt2, _, node2 = heappop(hq)
            new = HuffmanCode.Node(cnt1 + cnt2)
            new.left = node1
            new.right = node2
            heappush(hq, (new.cnt, id(new), new))

        return hq[0][2]

    def _build_code(self, node: "HuffmanCode.Node", path: str) -> None:
        if node.char is not None:
            self._code[node.char] = path or "0"  # 1文字専用対策
            return
        self._build_code(node.left, path + "0")
        self._build_code(node.right, path + "1")

    def get_code(self, char: str) -> str:
        """アルファベットの符号を返す"""
        assert char in self._code, f"{char} does not exist"
        return self._code[char]

    def get_char(self, code: str) -> str:
        """符号をアルファベットに復元"""
        node = self._root
        out = []
        for bit in code:
            node = node.left if bit == "0" else node.right
            if node.char is not None:
                out.append(node.char)
                node = self._root
        return "".join(out)