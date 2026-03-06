class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class BST:
    def __init__(self):
        self.root = None

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
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(value)
                    node.right.parent = node
                    return
                node = node.right

    def discard(self,value):
        """存在したならtrue,しなかったならfalse"""
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
            del node
        return True

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


t = BST()
for _ in range(int(input())):
    q,v = map(int,input().split())
    if q == 0:
        t.add(v)
    elif q == 1:
        print("Yes" if v in t else "No")
    else:
        print("Complete" if t.discard(v) else "Error")