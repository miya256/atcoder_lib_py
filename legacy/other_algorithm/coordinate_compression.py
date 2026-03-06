from bisect import bisect_left, bisect
class Compressor:
    def __init__(self, num):
        self.num = sorted([i for i in set(num)])
        self.compressed = {v:i for i,v in enumerate(self.num)}
    
    def __len__(self):
        return len(self.num)

    def original(self, comp):
        """圧縮後の値から元の値を返す"""
        return self.num[comp]

    def compress(self, orig):
        """元の値から圧縮後の値を返す"""
        if orig not in self.compressed:
            self.compressed[orig] = bisect_left(self.num, orig)
        return self.compressed[orig]
    
    def __call__(self, orig):
        return self.compress(orig)


"""添え字
更新クエリをnumに入れる
取得クエリのl,rはいれなくてよい

更新クエリのindex = [p1,p2,...] そのままいれる(-1とかしない)

set(compressed[p],x)
prod(compressed[l],compressed[r])
クエリを処理するときも-1とかしないで、p,l,rを使う
"""