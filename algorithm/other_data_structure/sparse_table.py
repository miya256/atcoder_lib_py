#冪等性が必要なのでmax,minとかはOK、sumとかはダメ
class SparseTable:
    def __init__(self,op,a):
        """a: 配列"""
        self.op = op
        self.a = [a]
        for i in range((len(a)-1).bit_length()-1):
            tmp = []
            for j in range(0,len(self.a[-1])-2**i):
                tmp.append(self.op(self.a[-1][j],self.a[-1][j+2**i]))
            self.a.append(tmp)
    
    def prod(self,l,r):
        """[l,r)までopした結果"""
        if r-l == 1:
            return self.a[0][l]
        idx = (r-l-1).bit_length()-1
        return self.op(self.a[idx][l],self.a[idx][r-2**idx])
