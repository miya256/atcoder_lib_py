"""
suffix arrayクラス
インスタンス化時にSA-ISによりSAを構築

LCP arrayを作成するメソッドや
SA上の二分探索などを実装
"""

"""
L,S,LMSつける
LMSをバケットソート
L,Sをinduced sort

文字を数字にしてからやる
"""

class SuffixArray:
    def __init__(self, string):
        self.n = len(string) + 1
        self.string = string.lower()
        self.suffix_array = self._build()
    
    def _build(self):
        array = [ord(char)-ord('a')+1 for char in self.string]
        array.append(0)
        return self._sa_is(array)
    
    def _calc_bounds(self, array):
        counter = [0] * (max(array)+1)
        for i in array:
            counter[i] += 1
        for i in range(len(counter)-1):
            counter[i+1] += counter[i]
        return [0]+counter[:-1], counter
    
    def is_l_type(self, array, i):
        return array[i] >= array[i+1]
    
    def is_s_type(self, array, i):
        return array[i] < array[i+1]
    
    def is_lms_type(self, array, i):
        return self.is_l_type(array, i-1) and self.is_s_type(array, i)

    def _sa_is(self, array):
        start, end = self._calc_bounds(array)
        sa = [-1] * len(array)

        #LMSを入れる
        for i in range(len(array)):
            if self.is_lms_type(array, i):
                end[array[i]] -= 1
                sa[end[array[i]]] = i
        
        #Lをいれる、LMSを削除
        for i in range(len(sa)):
            if sa[i] != -1 and self.is_l_type(array, sa[i]-1):
                start[array[sa[i]-1]] = sa[i]-1
                start[array[sa[i]-1]] += 1
            if self.is_lms_type(array, sa[i]):
                end[array[sa[i]]] = -1
                end[array[sa[i]]] += 1
        
        #Sを入れる
        for i in range(len(sa)-1,-1,-1):
            if sa[i] != -1 and self.is_s_type(array, sa[i]-1):
                end[array[sa[i]-1]] -= 1
                end[array[sa[i]-1]] = sa[i]-1
        
        return sa