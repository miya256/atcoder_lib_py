class BinaryTrie:
    class Node:
        def __init__(self):
            self.ch = [None, None] #左子、右子
            self.count = 0 #ここを通る数の個数
        
        def __getitem__(self, bit):
            return self.ch[bit]
        
        def __setitem__(self, bit, node):
            self.ch[bit] = node

    def __init__(self, d):
        self.d = d #桁数
        self.root = BinaryTrie.Node()
    
    def add(self, binary):
        cur = self.root
        cur.count += 1
        for i in range(self.d-1, -1, -1):
            bit = binary >> i & 1
            if cur[bit] is None:
                cur[bit] = BinaryTrie.Node()
            cur = cur[bit]
            cur.count += 1
    
    def discard(self, binary):
        cur = self.root
        cur.count -= 1
        for i in range(self.d-1, -1, -1):
            cur = cur[binary >> i & 1]
            cur.count -= 1