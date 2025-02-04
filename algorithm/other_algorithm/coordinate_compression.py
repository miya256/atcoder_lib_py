import bisect
class Shrink:
    def __init__(self,num):
        self.num = sorted([i for i in set(num)])

    def val(self,shr):
        """圧縮後の値から元の値を返す"""
        return self.num[shr]

    def shr(self,val):
        """元の値から圧縮後の値を返す"""
        return bisect.bisect_left(self.num,val)
    
    def __getitem__(self,val):
        return self.shr(val)


"""添え字
更新クエリをnumに入れる
取得クエリのl,rはいれなくてよい

更新クエリのindex = [p1,p2,...] そのままいれる(-1とかしない)

set(shr[p],x)
prod(shr[l],shr[r])
クエリを処理するときも-1とかしないで、p,l,rを使う
"""