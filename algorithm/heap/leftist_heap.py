#併合可能
class LeftistNode:
    def __init__(self,val,left=None,right=None,dist=0):
        self.val = val
        self.left = left
        self.right = right
        self.dist = dist

class LeftistHeap:
    def __init__(self):
        self.root = None

    def heapmerge(self,h1,h2):
        if not h1: return h2
        if not h2: return h1
        if h1.val > h2.val:
            h1, h2 = h2, h1
        if not h1.left:
            h1.left = h2
        else:
            h1.right = self.heapmerge(h1.right,h2)
            if h1.left.dist < h1.right.dist:
                h1.left, h1.right = h1.right, h1.left
            h1.dist = h1.right.dist + 1
        return h1

    def heappush(self,val):
        self.root = self.heapmerge(LeftistNode(val), self.root)

    def heappop(self):
        if not self.root: raise Exception("Heap is empty")
        res = self.root.val
        self.root = self.heapmerge(self.root.left, self.root.right)
        return res

    def getmin(self):
        if self.root: return self.root.val
        else: raise Exception("Heap is empty")
