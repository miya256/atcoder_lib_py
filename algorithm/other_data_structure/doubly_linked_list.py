#同じ要素があるとダメ

class LinkedList:
    def __init__(self,a = None):
        self.prev = {"head":None,"tail":"head"}
        self.next = {"tail":None,"head":"tail"}
        if a:
            self.next["head"] = a[0]
            self.prev["tail"] = a[-1]
            a = ["head"]+a+["tail"]
            for i in range(1,len(a)-1):
                self.prev[a[i]] = a[i-1]
                self.next[a[i]] = a[i+1]
    
    def append(self, value):
        self.prev[value] = self.prev["tail"]
        self.next[value] = "tail"
        self.next[self.prev["tail"]] = value
        self.prev["tail"] = value
    
    def insert(self, value, prev = "head"):
        self.prev[value] = prev
        self.next[value] = self.next[prev]
        self.prev[self.next[prev]] = value
        self.next[prev] = value
    
    def remove(self, value):
        self.next[self.prev[value]] = self.next[value]
        self.prev[self.next[value]] = self.prev[value]
        del self.prev[value]
        del self.next[value]
