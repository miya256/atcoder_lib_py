import random

#hashのxorとかsumとかが等しければ同じ集合
class ZobristHash:
    def __init__(self,k):
        """k個の要素についてハッシュ値を生成"""
        self.mod = (1<<61)-1
        self.hash = random.sample(range(1,self.mod),k)
    
    def __getitem__(self,i):
        return self.hash[i]

k = 10**5
hash = ZobristHash(k)
print(hash[0])