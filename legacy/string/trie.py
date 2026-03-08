class Trie:
    class Node:
        """
        根からこのノードまでつなげた文字列を
        この文字列と呼ぶことにする
        """
        def __init__(self, char=""):
            self.char = char
            self.children = {}
            self.prefix_count = 0 #このprefixで始まる文字列の個数
            self.word_count = 0 #この文字列の個数
        
        def is_end(self):
            """ある文字列の最後の文字であるか"""
            return self.word_count > 0
        
        def __str__(self):
            return self.char

    def __init__(self):
        self.root = Trie.Node()
    
    def add(self, string):
        """文字列を追加"""
        self._add(string)
    
    def discard(self, string):
        """文字列を削除"""
        self._discard(string)
    
    def contains(self, string):
        """文字列が存在するか"""
        return self._contains(string)
    
    def __contains__(self, string):
        return self._contains(string)
    
    def contains_prefix(self, string):
        """stringの接頭辞である文字列が存在するか"""
        return self._contains_prefix(string)
    
    def count_lcp(self, string):
        """stringとのLCPの長さとその文字列の個数{長さ: 個数, }"""
        return self._count_lcp(string)
    
    def count_words_with_prefix(self, prefix):
        """prefixで始まる文字列の個数"""
        return self._count_words_with_prefix(prefix)
    
    def get_words_with_prefix(self, prefix):
        """prefixで始まる文字列を辞書順に列挙"""
        return self._get_words_with_prefix(prefix)
    
    def count_all_words(self):
        """この木に入っているすべての文字列の個数"""
        return self._count_words_with_prefix("")
    
    def enumerate_all_words(self):
        """すべての文字列を辞書順に列挙"""
        return self._get_words_with_prefix("")
    
    def get_kth_word(self, k):
        """辞書順でk番目の要素を取得(0-indexed)"""
        return self._get_kth_word(k)
    
    def __str__(self):
        return f'{self.enumerate_words()}'
    

    def _add(self, string):
        self.root.prefix_count += 1
        current = self.root
        for char in string:
            if char not in current.children:
                current.children[char] = Trie.Node(char)
            current = current.children[char]
            current.prefix_count += 1
        current.word_count += 1
    
    def _discard(self, string):
        if not self._contains(string):
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
    
    def _traverse(self, string):
        """stringに基づいてノードをたどる"""
        current = self.root
        for char in string:
            if char not in current.children:
                return None
            current = current.children[char]
        return current
    
    def _contains(self, string):
        node = self._traverse(string)
        if node is None:
            return False
        return node.is_end()
    
    def _contains_prefix(self, string):
        current = self.root
        for char in string:
            if char not in current.children:
                return False
            current = current.children[char]
            if current.is_end():
                return True
        return False
    
    def _count_lcp(self, string):
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
    
    def _count_words_with_prefix(self, prefix):
        node = self._traverse(prefix)
        if node is None:
            return 0
        return node.prefix_count
        
    def _get_words_with_prefix(self, prefix):
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
    
    def _get_kth_word(self, k):
        assert k < self.root.prefix_count, f'{k}th string is not found'
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