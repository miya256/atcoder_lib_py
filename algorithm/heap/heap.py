class Heap:
    def __init__(self, compare):
        self.heap = [None]
        self.compare = compare
    
    def __len__(self):
        return len(self.heap)-1
    
    def __getitem__(self, i):
        return self.heap[i+1]
    
    def add(self, value):
        self.heap.append(value)
        self._sift_up(len(self))
    
    def pop(self):
        assert len(self) > 0, "heap is empty"
        res = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.heap.pop()
        self._sift_down(1)
        return res
    
    def _sift_up(self, i):
        while i > 1:
            if self.compare(self.heap[i//2], self.heap[i]):
                break
            self.heap[i//2], self.heap[i] = self.heap[i], self.heap[i//2]
            i >>= 1
    
    def _sift_down(self, i):
        while True:
            smallest = i
            if i*2 <= len(self) and self.compare(self.heap[i*2], self.heap[smallest]):
                smallest = i*2
            if i*2+1 <= len(self) and self.compare(self.heap[i*2+1], self.heap[smallest]):
                smallest = i*2+1
            
            if smallest == i:
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

def compare(parent, child):
    """parent が child より優先されるなら True"""
    return parent < child