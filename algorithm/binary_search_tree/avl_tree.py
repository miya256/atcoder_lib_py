class Node:
    def __init__(self, value):
        self.value = value
        self.height = 1
        self.size = 1
        self.left = None
        self.right = None
        self.parent = None
    
    def __str__(self):
        return f'Node(v={self.value}, h={self.height}, s={self.size})'

class AVLTree:
    def __init__(self,root=None):
        self.root = root
    
    def _rotate_left(self,node):
        """node中心に左回転"""
        parent = node.parent
        pivot = node.right

        node.right = pivot.left
        if pivot.left:
            pivot.left.parent = node
            pivot.size -= pivot.left.size
        node.size -= pivot.size
        node.height = node.left.height + 1 if node.left else 1

        pivot.left = node
        node.parent = pivot
        pivot.size += node.size
        pivot.height = node.height + 1

        #親を根とした部分木の高さは変わらない
        if parent and parent.left == node:
            parent.left = pivot
        elif parent and parent.right == node:
            parent.right = pivot
        else:
            self.root = pivot
        pivot.parent = parent
    
    def _rotate_right(self,node):
        parent = node.parent
        pivot = node.left

        node.left = pivot.right
        if pivot.right:
            pivot.right.parent = node
            pivot.size -= pivot.right.size
        node.size -= pivot.size
        node.height = node.right.height + 1 if node.right else 1

        pivot.right = node
        node.parent = pivot
        pivot.size += node.size
        pivot.height = node.height + 1

        if parent and parent.left == node:
            parent.left = pivot
        elif parent and parent.right == node:
            parent.right = pivot
        else:
            self.root = pivot
        pivot.parent = parent
    
    def _balance(self,node):
        while node:
            hl, hr = 0, 0
            node.size = 1
            if node.left:
                hl = node.left.height
                node.size += node.left.size
            if node.right:
                hr = node.right.height
                node.size += node.right.size
            node.height = max(hl,hr) + 1
            if hl - hr < -1:
                if node.right.left and node.right.right and node.right.left.height - node.right.right.height >= 1:
                    self._rotate_right(node.right)
                    self._rotate_left(node)
                else:
                    self._rotate_left(node)
            elif hl - hr > 1:
                if node.left.left and node.left.right and node.left.left.height - node.left.right.height <= -1:
                    self._rotate_left(node.left)
                    self._rotate_right(node)
                else:
                    self._rotate_right(node)
            node = node.parent
    
    def add(self,value):
        node = self.root
        if node is None:
            self.root = Node(value)
            return
        while True:
            if value <= node.value:
                if node.left is None:
                    node.left = Node(value)
                    node.left.parent = node
                    break
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(value)
                    node.right.parent = node
                    break
                node = node.right
        self._balance(node)
        return
    
    def discard(self,value):
        """左の最大値か右の最小値と交換"""
        node = self.root
        while node:
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right
            else:
                break
        if node is None:
            return False
        if node.left and node.right:
            next_node = node.right
            while next_node.left:
                next_node = next_node.left
            next_value = next_node.value
            self.discard(next_value)
            node.value = next_value
            self._balance(node)
        else:
            parent = node.parent
            if not parent:
                if node.left:
                    self.root = node.left
                elif node.right:
                    self.root = node.right
                else:
                    self.root = None
            elif node.left:
                if parent.left == node:
                    parent.left = node.left
                else:
                    parent.right = node.left
                node.left.parent = parent
            elif node.right:
                if parent.left == node:
                    parent.left = node.right
                else:
                    parent.right = node.right
                node.right.parent = parent
            else:
                if parent.left == node:
                    parent.left = None
                else:
                    parent.right = None
            self._balance(parent)
            del node
        return True
    
    def _get_node(self,i):
        """i番目のノードを返す"""
        node = self.root
        while True:
            if node.left and i < node.left.size:
                node = node.left
            elif node.left and i > node.left.size:
                i -= node.left.size + 1
                node = node.right
            elif not node.left and i > 0:
                i -= 1
                node = node.right
            else:
                return node
    
    def __getitem__(self,i):
        return self._get_node(i).value

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.size

    def __contains__(self, value):
        node = self.root
        while node:
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right
            else:
                return True
        return False
    
    def pop(self,i=-1):
        if i == -1:
            i += self.root.size
        value = self._get_node(i).value
        self.discard(value)
        return value

    def bisect_left(self,x):
        idx = 0
        node = self.root
        while node:
            if x <= node.value:
                node = node.left
            else:
                idx += node.left.size + 1 if node.left else 1
                node = node.right
        return idx

    def bisect_right(self,x):
        idx = 0
        node = self.root
        while node:
            if x < node.value:
                node = node.left
            else:
                idx += node.left.size + 1 if node.left else 1
                node = node.right
        return idx
        
    def index(self,x):
        assert x in self
        return self.bisect_left(x)
    
    def _dfs(self,node,i,array):
        if i >= self.root.height:
            return
        if node is None:
            array[i].append(None)
            return
        self._dfs(node.left,i+1,array)
        array[i].append(str(node))
        self._dfs(node.right,i+1,array)
    
    """
    @staticmethod
    def _merge(l,root,r):
        if -1 <= l.height - r.height <= 1:
            root.left = l
            root.right = r
            return root
        elif l.height - r.height > 0:
            l.right = AVLTree._merge(l.right,root,r)
            return l
        else:
            r.left = AVLTree._merge(l,root,r.left)
            return r

    @staticmethod
    def merge(l,r):
        #max(l) <= min(r)の必要がある
        if not l: return r
        if not r: return l
        root = Node(l.pop())
        return AVLTree._merge(l.root,root,r.root)
    
    def split()

    [1,2,5,6],[3,4,7,8]をマージするときは、
    [1,2],[5,6],[3,4],[7,8]にsplitしてからマージする
    ->[1,2,3,4],[5,6],[7,8]
    ->[1,2,3,4,5,6],[7,8]
    ->[1,2,3,4,5,6,7,8]
    """
    
    def __str__(self):
        array = [[] for _ in range(self.root.height)]
        self._dfs(self.root,0,array)
        array = '\n'.join(list(map(str,array)))
        return array



t1 = AVLTree()
t2 = AVLTree()
for i in range(5):
    t1.add(i)
    t2.add(i+5)
t = AVLTree(t1,t2)
print(t)