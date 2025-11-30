class Trie:
    """
    多重集合

    Methods:
        add(string)                    : 文字列を追加。O(|S|)
        discard(string)                : 文字列を削除。O(|S|)
        contains(string)               : 文字列が存在するか。O(|S|)
        contains_prefix(string)        : stringの接頭辞である文字列が存在するか。O(|S|)
        count_lcp(string)              : stringとのLCPの長さが i である文字列の個数。O(|S|)
        count_words_with_prefix(prefix): prefixで始まる文字列の個数。O(|S|)
        get_words_with_prefix(prefix)  : prefixで始まる文字列を辞書順に列挙。計算量は、答えとなる文字列の長さの合計
        count_all_words()              : この木に入っているすべての文字列の個数。O(1)
        get_all_words()                : すべての文字列を辞書順に列挙。計算量は、答えとなる文字列の長さの合計
        get_kth_word(k)                : 辞書順でk番目の要素を取得(0-indexed)。O(木の高さ)？
    """
    class Node:
        """
        根からこのノードまでつなげた文字列を
        この文字列と呼ぶことにする

        Attributes:
            char        : このノードの文字
            children    : 子ノード
            prefix_count: この文字列がprefixである文字列の個数
            word_count  : この文字列の個数
        """
        def __init__(self, char: str = "") -> None:
            self.char = char
            self.children = {} #長さ26の配列も試したが、あまり変わらず
            self.prefix_count = 0
            self.word_count = 0
        
        def is_end(self) -> bool:
            """ある文字列の最後の文字であるか"""
            return self.word_count > 0
        
        def __repr__(self) -> str:
            return self.char
    
    def __init__(self) -> None:
        self.root = Trie.Node()

    def __len__(self) -> int:
        """文字列の個数"""
        return self.count_all_words()
    
    def __contains__(self, string: str) -> bool:
        """stringが存在するか"""
        return self.contains(string)
    
    def __getitem__(self, k: int) -> str:
        """辞書順でk番目の要素を取得(0-indexed)"""
        return self.get_kth_word(k)
    
    def __repr__(self) -> str:
        return f'Trie {self.get_all_words()}'
    
    def add(self, string: str) -> None:
        """stringを追加"""
        self.root.prefix_count += 1
        current = self.root
        for char in string:
            if char not in current.children:
                current.children[char] = Trie.Node(char)
            current = current.children[char]
            current.prefix_count += 1
        current.word_count += 1
    
    def discard(self, string: str) -> None:
        """stringを削除"""
        if not self.contains(string):
            return
        self.root.prefix_count -= 1
        current = self.root
        for char in string:
            current.children[char].prefix_count -= 1
            if current.children[char].prefix_count == 0:
                del current.children[char]
                return
            current = current.children[char]
        current.word_count -= 1
    
    def contains(self, string: str) -> bool:
        """stringが存在するか"""
        node = self._traverse(string)
        if node is None:
            return False
        return node.is_end()
    
    def contains_prefix(self, string: str) -> bool:
        """stringの接頭辞である文字列が存在するか"""
        current = self.root
        for char in string:
            if char not in current.children:
                return False
            current = current.children[char]
            if current.is_end():
                return True
        return False
    
    def count_lcp(self, string: str) -> list[int]:
        """stringとのLCPの長さが i である文字列の個数"""
        current = self.root
        #先頭i文字が等しい文字列の個数を数えてから
        lcp_count = [self.count_all_words()] + [0] * len(string)
        for i, char in enumerate(string, 1):
            if char not in current.children:
                break
            current = current.children[char]
            lcp_count[i] = current.prefix_count

        for i in range(len(string)):
            lcp_count[i] -= lcp_count[i+1]
        return lcp_count
    
    def count_words_with_prefix(self, prefix: str) -> int:
        """prefixで始まる文字列の個数"""
        node = self._traverse(prefix)
        if node is None:
            return 0
        return node.prefix_count
    
    def get_words_with_prefix(self, prefix: str) -> list[str]:
        """prefixで始まる文字列を辞書順に列挙"""
        node = self._traverse(prefix)
        if node is None:
            return []

        words = []
        word = [prefix[:-1]]
        stack = [node]
        while stack: #dfs
            node = stack.pop()
            if node is None: #帰りなら
                word.pop()
                continue
            word.append(node.char)
            #ノードが終端ならその数だけ答えに追加
            words.extend([''.join(word) for _ in range(node.word_count)])
            stack.append(None) #帰り用
            for _, next in sorted(node.children.items(), reverse=True):
                stack.append(next)
        return words
    
    def count_all_words(self) -> int:
        """この木に入っているすべての文字列の個数"""
        return self.count_words_with_prefix("")
    
    def get_all_words(self) -> list[str]:
        """すべての文字列を辞書順に列挙"""
        return self.get_words_with_prefix("")
    
    def get_kth_word(self, k: int) -> str:
        """辞書順でk番目の要素を取得(0-indexed)"""
        assert k < self.count_all_words(), f'{k}th string is not found'
        current = self.root
        string = []
        while k >= 0:
            for char, node in sorted(current.children.items()):
                if node.prefix_count > k:
                    current = node
                    string.append(char)
                    k -= current.word_count
                    break
                k -= node.prefix_count
        return ''.join(string)
    
    def _traverse(self, string: str) -> Node | None:
        """stringに基づいてノードをたどる"""
        current = self.root
        for char in string:
            if char not in current.children:
                return None
            current = current.children[char]
        return current