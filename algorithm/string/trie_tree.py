class TrieTree:
    class Node:
        def __init__(self,s):
            self.s = s
            self.isend = False
            self.children = {}

    def __init__(self):
        self.root = self.Node("")

    def add(self,s):
        node = self.root
        for t in s:
            if t in node.children:
                node = node.children[t]
            else:
                node.children[t] = self.Node(t)
                node = node.children[t]
        node.isend = True

    def search(self,prefix):
        """prefixで始まる文字列一覧を返す"""
        node = self.root
        for t in prefix: #prefixまで潜る
            if t not in node.children:
                return []
            node = node.children[t]
        res = [] #prefixより下をdfs
        stack = [(node,prefix)]
        while stack:
            node,prefix = stack.pop()
            if node.isend:
                res.append(prefix)
                continue
            for s,ch in node.children.items():
                stack.append((ch,prefix+s))
        return res