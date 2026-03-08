class Accumulate:
    def __init__(self, a):
        self.acc = [0]
        for i in a:
            self.acc.append(self.acc[-1] + i)

    def query(self, l, r):
        """[l,r)"""
        return self.acc[r] - self.acc[l]


class Accumulate_2D:
    def __init__(self, a):
        x, y = len(a), len(a[0])
        self.acc = [[0] * (y+1) for _ in range(x+1)]
        for i in range(x):
            for j in range(y):
                self.acc[i+1][j+1] = a[i][j]

        for i in range(x+1):
            for j in range(y):
                self.acc[i][j+1] += self.acc[i][j]
        for j in range(y+1):
            for i in range(x):
                self.acc[i+1][j] += self.acc[i][j]

    def query(self, l, r):
        res = 0
        res += self.acc[l[0]][l[1]]
        res -= self.acc[l[0]][r[1]]
        res -= self.acc[r[0]][l[1]]
        res += self.acc[r[0]][r[1]]
        return res


class Accumulate_3D:
    def __init__(self, a):
        x, y, z = len(a), len(a[0]), len(a[0][0])
        self.acc = [[[0] * (z+1) for _ in range(y+1)] for _ in range(x+1)]
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    self.acc[i+1][j+1][k+1] = a[i][j][k]

        for i in range(x+1):
            for j in range(y+1):
                for k in range(z):
                    self.acc[i][j][k+1] += self.acc[i][j][k]
        for i in range(x+1):
            for k in range(z+1):
                for j in range(y):
                    self.acc[i][j+1][k] += self.acc[i][j][k]
        for j in range(y+1):
            for k in range(z+1):
                for i in range(x):
                    self.acc[i+1][j][k] += self.acc[i][j][k]

    def query(self, l, r):
        res = 0
        res -= self.acc[l[0]][l[1]][l[2]]
        res += self.acc[l[0]][l[1]][r[2]]
        res += self.acc[l[0]][r[1]][l[2]]
        res -= self.acc[l[0]][r[1]][r[2]]
        res += self.acc[r[0]][l[1]][l[2]]
        res -= self.acc[r[0]][l[1]][r[2]]
        res -= self.acc[r[0]][r[1]][l[2]]
        res += self.acc[r[0]][r[1]][r[2]]
        return res


class Accumulate:
    def __init__(self,a):
        self.acc = self._build(a)
    
    def _build(self,a):
        if isinstance(a,int):
            return a
        acc = [self._zero_array(a[0])]
        for i in a:
            acc.append(self._sum(acc[-1], self._build(i)))
        return acc
    
    def _zero_array(self,a):
        if isinstance(a,int):
            return 0
        return [self._zero_array(a[0]) for _ in range(len(a)+1)]
    
    def _sum(self,a,b):
        if isinstance(a,int):
            return a+b
        for i in range(len(a)):
            b[i] = self._sum(a[i],b[i])
        return b
    
    def _query(self,i,l,r,a):
        if isinstance(a,int):
            return a
        return self._query(i>>1,l[1:],r[1:],a[l[0]] if i&1 else a[r[0]])
    
    def query(self,l,r):
        res = 0
        for i in range(1<<len(l)):
            res += (-1)**i.bit_count() * self._query(i,l,r,self.acc)
        return res

acc_l = [0]*(n+1)
acc_r = [0]*(n+1)
for i in range(n):
    acc_l[i+1] = acc_l[i] + a[i]
for i in range(n):
    acc_r[-i-2] = acc_r[-i-1] + a[-i-1]
#acc_l[i] : [:i)
#acc_r[i] : [i:]
