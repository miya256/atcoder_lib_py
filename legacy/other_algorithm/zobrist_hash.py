import random

#hashのxorとかsumとかが等しければ同じ集合
class ZobristHash:
    def __init__(self,num):
        """numに含まれる要素のハッシュ値を生成"""
        self.mod = (1<<61)-1
        self.hash = {v:h for v,h in zip(set(num),random.sample(range(1,self.mod),len(set(num))))}
    
    def __getitem__(self,i):
        return self.hash[i]
    
    def __setitem__(self,i,v): #0のハッシュ値を0にするときとかに使う
        self.hash[i] = v