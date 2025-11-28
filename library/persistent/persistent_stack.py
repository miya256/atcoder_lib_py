class PersistentStack:
    class Node:
        def __init__(self, value):
            self.value = value
            self.parent = None

    def __init__(self):
        self.tail = None
        self.version = dict()
    
    def get(self):
        """末尾の要素を取得"""
        return self.tail.value
    
    def push(self,value):
        new = self.Node(value)
        new.parent = self.tail
        self.tail = new
    
    def pop(self):
        assert self.tail,"stack is empty"
        value = self.tail.value
        self.tail = self.tail.parent
        return value
    
    def save(self,key):
        """keyに今の状態を保存"""
        self.version[key] = self.tail
    
    def load(self,key):
        """stackをkeyの状態にする"""
        assert key in self.version,f'{key}に対応するversionは存在しません'
        self.tail = self.version[key]
    
    def isempty(self):
        return self.tail is None