#冪等性が必要なのでmax,minとかはOK、sumとかはダメ
class SparseTable:
    def __init__(self, op, a):
        """a: 配列"""
        self.op = op
        self.a = [[(v, i) for i, v in enumerate(a)]]
        for i in range(1, len(a).bit_length()):
            self.a.append([0] * (len(a)-(1<<i)+1))
            for j in range(len(a)-(1<<i)+1):
                self.a[i][j] = self.op(self.a[i-1][j],self.a[i-1][j+(1<<(i-1))])
    
    def prod(self, l, r):
        """[l,r)までopした結果(値, index)"""
        idx = (r-l).bit_length() - 1
        return self.op(self.a[idx][l], self.a[idx][r-(1<<idx)])