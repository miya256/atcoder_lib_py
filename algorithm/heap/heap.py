class Heap:
    def __init__(self,key=lambda x:x):
        self.heap = [None]
        self.key = key
    
    def __len__(self):
        return len(self.heap)-1
    
    def __getitem__(self,i):
        return self.heap[i+1]
    
    def push(self,value):
        self.heap.append(value)
        i = len(self)
        while i > 1:
            if self.key(self.heap[i]) < self.key(self.heap[i//2]):
                self.heap[i//2],self.heap[i] = self.heap[i],self.heap[i//2]
            i >>= 1
    
    def pop(self):
        assert len(self) != 0, "heap is empty"
        res = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.heap.pop()
        i = 1
        while True:
            if i*2 > len(self): #子がいないなら終わり
                return res
            if i*2+1 > len(self): #左だけいるなら、左の子のほうが小さければ入れ替えて終わり
                if self.key(self.heap[i*2]) < self.key(self.heap[i]):
                    self.heap[i*2],self.heap[i] = self.heap[i],self.heap[i*2]
                return res
            if self.key(self.heap[i*2]) < self.key(self.heap[i*2+1]):
                if self.key(self.heap[i*2]) < self.key(self.heap[i]):
                    self.heap[i*2],self.heap[i] = self.heap[i],self.heap[i*2]
                i = i*2
            else:
                if self.key(self.heap[i*2+1]) < self.key(self.heap[i]):
                    self.heap[i*2+1],self.heap[i] = self.heap[i],self.heap[i*2+1]
                i = i*2+1