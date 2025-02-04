#一番最初に生成するときは、値を指定しない
#h = SkewHeap()　をつくってからhpushで値を入れる
#併合可能
class SkewHeap:
    def __init__(self,val = None):
        self.val = val
        self.left = None
        self.right = None
        self.root = None

    def heapmerge(self,h1,h2):
        if h1 is None: return h2
        if h2 is None: return h1
        if h1.val is None: return h2
        if h2.val is None: return h1
        if h1.val > h2.val:
            h1.val, h1.left, h1.right, h2.val, h2.left, h2.right\
                    = h2.val, h2.left, h2.right, h1.val, h1.left, h1.right
        h1.right = self.heapmerge(h2,h1.right)
        h1.left, h1.right = h1.right, h1.left
        return h1

    def heappush(self,val):
        self.root = self.heapmerge(self.root,SkewHeap(val))

    def heappop(self):
        res = self.root.val
        self.root = self.heapmerge(self.root.left,self.root.right)
        return res
        
