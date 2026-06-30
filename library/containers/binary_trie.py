class BinaryTrie:
    """
    Binary Trie

    Methods:
        add(x)     : x を追加
        discard(x) : x を削除
        contains(x): x が存在するか

        xor引数付き (
            key = lambda v: v ^ xor でsortしてあるとみなす
            a[i]^xor と x を比較している感じ
        )
        kth_smallest(k): 小さいほうからk番目の値 (0-indexed)
        kth_largest(k) : 大きいほうからk番目の値 (0-indexed)
        bisect_left(x) : x以上の最小値のindex
        bisect_right(x): x超過の最小値のindex
        lt(x)          : xより小さい最大値
        le(x)          : x以下の最大値
        gt(x)          : xより大きい最小値
        ge(x)          : x以上の最小値
        apply_xor(mask): 全体にmaskをxorする
    """

    class Node:
        def __init__(self):
            self.child: tuple[BinaryTrie.Node, BinaryTrie.Node] | None = None
            self.count = 0
            self.xor_mask = 0

    def __init__(self, bit_length: int):
        self._bit_length = bit_length
        self._root = BinaryTrie.Node()

    def __len__(self) -> int:
        return self._root.count

    def __contains__(self, x: int) -> bool:
        return self.contains(x)

    def __getitem__(self, k: int) -> int:
        assert -self.__len__() <= k < self.__len__()
        if k < 0:
            k += self.__len__()
        return self.kth_smallest(k)

    def __repr__(self) -> str:
        numbers = []
        stack = [(self._root, 0, self._bit_length - 1)]
        while stack:
            node, value, i = stack.pop()
            self._push(node, i)
            if node.count > 0 and i == -1:
                numbers.append(value)
                continue
            if node.count == 0 or node.child is None:
                continue
            stack.append((node.child[1], (value << 1) + 1, i - 1))
            stack.append((node.child[0], value << 1, i - 1))
        return f"BinaryTrie({numbers})"

    def add(self, x: int) -> None:
        assert 0 <= x < 1 << self._bit_length
        self._root.count += 1
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            self._push(current, i)
            bit = x >> i & 1
            if current.child is None:
                current.child = (BinaryTrie.Node(), BinaryTrie.Node())
            current = current.child[bit]
            current.count += 1

    def discard(self, x: int) -> None:
        if not self.contains(x):
            return
        self._root.count -= 1
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            assert current.child is not None
            self._push(current, i)
            bit = x >> i & 1
            current = current.child[bit]
            current.count -= 1

    def contains(self, x: int) -> bool:
        """xが存在するか"""
        if not (0 <= x < 1 << self._bit_length):
            return False
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            self._push(current, i)
            bit = x >> i & 1
            if current.child is None:
                return False
            current = current.child[bit]
        return current.count > 0

    def kth_smallest(self, k: int, xor: int = 0) -> int:
        """k番目に小さい要素を取得"""
        assert 0 <= xor < 1 << self._bit_length
        assert 0 <= k < self._root.count
        value = 0
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            assert current.child is not None
            self._push(current, i)
            bit = xor >> i & 1
            if current.child[bit].count > k:
                current = current.child[bit]
                value |= bit << i
            else:
                k -= current.child[bit].count
                current = current.child[bit ^ 1]
                value |= (bit ^ 1) << i
        return value

    def kth_largest(self, k: int, xor: int = 0) -> int:
        """k番目に大きい要素を取得"""
        assert 0 <= xor < 1 << self._bit_length
        assert 0 <= k < self._root.count
        value = 0
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            assert current.child is not None
            self._push(current, i)
            bit = xor >> i & 1
            if current.child[bit ^ 1].count > k:
                current = current.child[bit ^ 1]
                value |= (bit ^ 1) << i
            else:
                k -= current.child[bit ^ 1].count
                current = current.child[bit]
                value |= bit << i
        return value

    def bisect_left(self, x: int, xor: int = 0) -> int:
        """x以上の最小値が何番目か"""
        assert 0 <= x < 1 << self._bit_length
        assert 0 <= xor < 1 << self._bit_length
        j = 0
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            if current.child is None:
                return j
            self._push(current, i)
            bit = xor >> i & 1
            if x >> i & 1:
                j += current.child[bit].count
                current = current.child[bit ^ 1]
            else:
                current = current.child[bit]
        return j

    def bisect_right(self, x: int, xor: int = 0) -> int:
        """xを超える最小値が何番目か"""
        assert 0 <= x < 1 << self._bit_length
        assert 0 <= xor < 1 << self._bit_length
        j = 0
        current = self._root
        for i in range(self._bit_length - 1, -1, -1):
            if current.child is None:
                return j
            self._push(current, i)
            bit = xor >> i & 1
            if x >> i & 1:
                j += current.child[bit].count
                current = current.child[bit ^ 1]
            else:
                current = current.child[bit]
        return j + current.count

    def lt(self, x: int, xor: int = 0) -> int | None:
        """xより小さい最大値"""
        assert 0 <= x < 1 << self._bit_length
        assert 0 <= xor < 1 << self._bit_length
        i = self.bisect_left(x, xor)
        if i == 0:
            return None
        return self.kth_smallest(i - 1, xor)

    def le(self, x: int, xor: int = 0) -> int | None:
        """x以下の最大値"""
        assert 0 <= x < 1 << self._bit_length
        assert 0 <= xor < 1 << self._bit_length
        i = self.bisect_right(x, xor)
        if i == 0:
            return None
        return self.kth_smallest(i - 1, xor)

    def ge(self, x: int, xor: int = 0) -> int | None:
        """x以上の最小値"""
        assert 0 <= x < 1 << self._bit_length
        assert 0 <= xor < 1 << self._bit_length
        i = self.bisect_left(x, xor)
        if i == len(self):
            return None
        return self.kth_smallest(i, xor)

    def gt(self, x: int, xor: int = 0) -> int | None:
        """xより大きい最小値"""
        assert 0 <= x < 1 << self._bit_length
        assert 0 <= xor < 1 << self._bit_length
        i = self.bisect_right(x, xor)
        if i == len(self):
            return None
        return self.kth_smallest(i, xor)

    def apply_xor(self, mask: int) -> None:
        """全体にmaskをxorする"""
        assert 0 <= mask < 1 << self._bit_length
        self._root.xor_mask ^= mask

    def _push(self, node: "BinaryTrie.Node", i: int) -> None:
        if node.child is None:
            node.xor_mask = 0
            return
        xor = node.xor_mask
        if xor >> i & 1:
            node.child = (node.child[1], node.child[0])
            xor -= 1 << i
        node.xor_mask = 0
        node.child[0].xor_mask ^= xor
        node.child[1].xor_mask ^= xor
