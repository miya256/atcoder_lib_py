from collections import defaultdict

class Node:
    def __init__(self,value):
        self.value = value
        self.parent = None

class PersistentStack:
    def __init__(self):
        self.tail = None
        self.version = defaultdict(lambda:None)
    
    def get(self):
        """末尾の要素を取得"""
        return self.tail.value
    
    def add(self,value):
        new = Node(value)
        new.parent = self.tail
        self.tail = new
    
    def pop(self):
        assert self.tail
        value = self.tail.value
        self.tail = self.tail.parent
        return value
    
    def save(self,key):
        """keyに今の状態を保存"""
        self.version[key] = self.tail
    
    def load(self,key):
        """stackをkeyの状態にする"""
        self.tail = self.version[key]
    
    def isempty(self):
        return self.tail is None