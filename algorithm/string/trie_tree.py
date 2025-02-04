class TrieNode:
    def __init__(self,s):
        """
        s:文字列
        n:根からこの文字までを接頭辞として、この接頭辞がついた文字列の個数
        """
        self.s = s
        self.isend = False
        self.children = {}
        self.n = 1

class TrieTree:
    def __init__(self):
        self.root = TrieNode("")

    def insert(self,s):
        node = self.root
        for t in s:
            if t in node.children:
                node = node.children[t]
                node.n += 1
            else:
                newNode = TrieNode(t)
                node.children[t] = newNode
                node = newNode
        node.isend = True

    def dfs(self,node,pre):
        if node.isend:
            self.res.append((pre + node.s))
        for nv in node.children.values():
            self.dfs(nv,pre + node.s)

    def search(self,pre):
        """pre(何文字でも良い)で始まる文字列一覧を返す"""
        node = self.root
        for t in pre:
            if t in node.children:
                node = node.children[t]
            else:
                return []
        self.res = []
        self.dfs(node,pre[:-1])
        return self.res

    def countCP(self,s):
        """前からi文字が等しいものの個数一覧を返す"""
        res = {}
        node = self.root
        for i,t in enumerate(s):
            if t in node.children:
                node = node.children[t]
                res[i] = node.n
            else:
                return res
        return res
