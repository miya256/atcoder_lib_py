class PersistentArray:
    class Node:
        def __init__(self,l,r,value=None):
            self.value = value
            self.l = l #担当区間[l,r)
            self.r = r
            self.chl = None #左右の子
            self.chr = None
    
    def __init__(self,a):
        if isinstance(a,int):
            a = [0 for i in range(a)]
        self.root= self._build(a)
        self.size = len(a)
        self.version = dict()
    
    def _build(self,a):
        root = self.Node(0,1<<len(a).bit_length())
        stack = [root]
        while stack:
            node = stack.pop()
            if node.r - node.l == 1:
                if node.l < len(a):
                    node.value = a[node.l]
                continue
            mid = (node.l + node.r) // 2
            node.chl = self.Node(node.l,mid)
            node.chr = self.Node(mid,node.r)
            stack.append(node.chr)
            stack.append(node.chl)
        return root
    
    def __getitem__(self,i):
        """今のa[i]"""
        return self.get(i)
    
    def __setitem__(self,i,value):
        self.set(i,value)
    
    def get(self,i,key=None):
        """version[key]のa[i]。versionを指定しなければ今の"""
        node = self.root if key is None else self.version[key]
        while node.r - node.l > 1:
            if i < (node.l + node.r) // 2:
                node = node.chl
            else:
                node = node.chr
        return node.value
    
    def set(self,i,value,key=None):
        """version[key]のa[i]をvalueに。今の配列はこれになる"""
        node = self.root if key is None else self.version[key]
        new = self.Node(node.l,node.r)
        self.root = new
        while node.r - node.l > 1:
            if i < (node.l + node.r) // 2:
                new.chr = node.chr
                node = node.chl
                new.chl = self.Node(node.l,node.r)
                new = new.chl
            else:
                new.chl = node.chl
                node = node.chr
                new.chr = self.Node(node.l,node.r)
                new = new.chr
        new.value = value
    
    def save(self,key):
        """keyに今の状態を保存"""
        self.version[key] = self.root
    
    def load(self,key):
        """version[key]にする"""
        self.root = self.version[key]
    
    def __str__(self):
        a = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.r - node.l == 1:
                if node.value is not None:
                    a.append(node.value)
                continue
            stack.append(node.chr)
            stack.append(node.chl)
        return str(a)