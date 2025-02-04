class Deque: #ランダムアクセス可能
    def __init__(self,data = []):
        self.buffer = data + [None] * (1<<20 - len(data))
        self.head = 0
        self.tail = len(data) #[head, tail)に要素がある
    
    def _index(self, i):
        if not -len(self) <= i < len(self):
            raise IndexError('index out of range: ' + str(i))
        if i >= 0:
            return (self.head + i) % len(self.buffer)
        else:
            return (self.tail + i) % len(self.buffer)
    
    def _extend(self):
        head = self.head
        buflen = len(self.buffer)
        new_buffer = self.buffer[head % buflen:] + self.buffer[:head % buflen] + [None]*buflen
        self.head -= head
        self.tail -= head
        self.buffer = new_buffer
    
    def __getitem__(self, i):
        return self.buffer[self._index(i)]
    
    def __setitem__(self, i, val):
        self.buffer[self._index(i)] = val
    
    def __len__(self):
        return self.tail - self.head
    
    def isfull(self):
        return len(self) == len(self.buffer)
    
    def isempty(self):
        return len(self) == 0
    
    def appendleft(self, val):
        if self.isfull(): self._extend()
        self.head -= 1
        self.buffer[self.head % len(self.buffer)] = val
    
    def append(self, val):
        if self.isfull(): self._extend()
        self.buffer[self.tail % len(self.buffer)] = val
        self.tail += 1
    
    def popleft(self):
        assert not self.isempty(), "deque is empty"
        val = self.buffer[self.head % len(self.buffer)]
        self.head += 1
        return val
    
    def pop(self):
        assert not self.isempty(), "deque is empty"
        self.tail -= 1
        val = self.buffer[self.tail % len(self.buffer)]
        return val
    
    def __str__(self):
        return f'Deque({list(self)})'