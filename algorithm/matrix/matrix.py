from copy import deepcopy
class Matrix:
    def __init__(self,matrix):
        """n行m列"""
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.matrix = matrix
        self.mod = 998244353
    
    def __getitem__(self,i):
        return self.matrix[i]
    
    def __mul__(self,other):
        assert isinstance(other,Matrix)
        assert self.m == other.n
        res = Matrix([[0]*other.m for _ in range(self.n)])
        for i in range(self.n):
            for j in range(other.m):
                for k in range(other.n):
                    res[i][j] += self[i][k] * other[k][j]
                res[i][j] %= self.mod
        return res
    
    def __pow__(self,other):
        assert self.n == self.m
        assert isinstance(other,int)
        res = Matrix([[0]*self.n for _ in range(self.n)])
        for i in range(self.n):
            res[i][i] = 1
        while other > 0:
            if other & 1:
                res *= self
            self *= self
            other >>= 1
        return res
    
    def __len__(self):
        return self.n
    
    def row(self):
        return self.n
    
    def column(self):
        return self.m
    
    def rotate(self,degree):
        """時計回り"""
        assert degree in (90,180,270)
        if degree == 180:
            new = [[0]*self.m for _ in range(self.n)]
        else:
            new = [[0]*self.n for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                if degree == 90: new[j][-i-1] = self[i][j]
                elif degree == 180: new[-i-1][-j-1] = self[i][j]
                else: new[-j-1][i] = self[i][j]
        if not degree == 180:
            self.n,self.m = self.m,self.n
        self.matrix = new
    
    def transpose(self):
        new = [[0]*self.n for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                new[j][i] = self[i][j]
        self.matrix = new
    
    def __str__(self):
        res = []
        for vector in self.matrix:
            res.append(str(vector))
        res = '\n '.join(res)
        return "[" + res + "]"

ma = [[1,1],[1,0]]
ma = Matrix(ma)
m1 = Matrix([[1,1,1],[2,2,1],[3,1,1],[5,4,7]])
for i in range(10):
    print((ma ** i))