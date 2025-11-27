class Matrix:
    """
    n*m行列 mod限定

    Attributes:
        n: 行数
        m: 列数
    
    Methods:
        getitem[i,j]: i,j成分
        setitem[i,j]: i,jに代入
        +, -, *, **, +=, -=, *=, **=, ==, != 演算子
        inverse         : 逆行列
        transpose       : 転置行列
        join_columns    : 横に行列を結合
        join_rows       : 縦に行列を結合
        swap_rows       : i行目とj行目を入れ替える（破壊的）
        multiply_row    : i行目をk倍する（破壊的）
        add_row_multiple: i行目にj行目のk倍を足す（破壊的）
    """
    Mod: int = 998244353

    def __init__(self, a: list[list[int]], mod: int = 0) -> None:
        if mod:
            Matrix.Mod = mod
        self.n = len(a)
        self.m = len(a[0])
        self._a = [a[i][j] for i in range(self.n) for j in range(self.m)]
    
    def __getitem__(self, indices: tuple[int, int]) -> int:
        """(i,j)成分"""
        assert isinstance(indices, tuple) and len(indices) == 2, f"shape error: indices={indices}"
        assert 0 <= indices[0] < self.n and 0 <= indices[1] < self.m, f"index error: (i,j)={indices}"
        return self._a[indices[0] * self.m + indices[1]]
    
    def __setitem__(self, indices: tuple[int, int], value: int):
        """(i,j)成分"""
        assert isinstance(indices, tuple) and len(indices) == 2, f"shape error: indices={indices}"
        assert 0 <= indices[0] < self.n and 0 <= indices[1] < self.m, f"index error: (i,j)={indices}"
        self._a[indices[0] * self.m + indices[1]] = value
    
    def __add__(self, other: "Matrix") -> "Matrix":
        """加算"""
        assert self.n == other.n and self.m == other.m, f"shape is not same: ({self.n},{self.m}) and ({other.n},{other.m})"
        data = [(self._a[i] + other._a[i]) % Matrix.Mod for i in range(self.n * self.m)]
        return Matrix._from_vector(data, self.n, self.m)
    
    def __sub__(self, other: "Matrix") -> "Matrix":
        """減算"""
        assert self.n == other.n and self.m == other.m, f"shape is not same: ({self.n},{self.m}) and ({other.n},{other.m})"
        data = [(self._a[i] - other._a[i]) % Matrix.Mod for i in range(self.n * self.m)]
        return Matrix._from_vector(data, self.n, self.m)
    
    def __mul__(self, other: "Matrix") -> "Matrix":
        """行列積"""
        assert self.m == other.n, f"shape error: ({self.n},{self.m}) and ({other.n},{other.m})"
        n, m, l = self.n, other.m, self.m
        data = [
            sum(self[i,k] * other[k,j] for k in range(l)) % Matrix.Mod
            for i in range(n) for j in range(m)
        ]
        return Matrix._from_vector(data, n, m)
    
    def __pow__(self, exp: int) -> "Matrix":
        assert self.n == self.m, f"shape error: ({self.n},{self.m})"
        if exp < 0:
            return self.inverse() ** (-exp)
        data = [int(i==j) for i in range(self.n) for j in range(self.m)]
        res = Matrix._from_vector(data, self.n, self.m)
        base = self
        while exp:
            if exp & 1:
                res *= base
            base = base * base
            exp >>= 1
        return res
    
    def __iadd__(self, other: "Matrix") -> "Matrix":
        assert self.n == other.n and self.m == other.m, f"shape is not same: ({self.n},{self.m}) and ({other.n},{other.m})"
        for i in range(self.n * self.m):
            self._a[i] += other._a[i]
            self._a[i] %= Matrix.Mod
        return self
    
    def __isub__(self, other: "Matrix") -> "Matrix":
        assert self.n == other.n and self.m == other.m, f"shape is not same: ({self.n},{self.m}) and ({other.n},{other.m})"
        for i in range(self.n * self.m):
            self._a[i] -= other._a[i]
            self._a[i] %= Matrix.Mod
        return self
    
    def __imul__(self, other: "Matrix") -> "Matrix":
        assert self.m == other.n, f"shape error: ({self.n},{self.m}) and ({other.n},{other.m})"
        n, m, l = self.n, other.m, self.m
        data = [
            sum(self[i,k] * other[k,j] % Matrix.Mod for k in range(l)) % Matrix.Mod
            for i in range(n) for j in range(m)
        ]
        self.n = n
        self.m = m
        self._a = data
        return self
    
    def __ipow__(self, exp: int) -> "Matrix":
        assert self.n == self.m, f"shape error: ({self.n},{self.m})"
        if exp < 0:
            res = self.inverse() ** (-exp)
            self._a = res._a
            return self
        data = [int(i==j) for i in range(self.n) for j in range(self.m)]
        res = Matrix._from_vector(data, self.n, self.m)
        base = self
        while exp:
            if exp & 1:
                res *= base
            base = base * base
            exp >>= 1
        self._a = res._a
        return self
    
    def __eq__(self, other: "Matrix") -> bool:
        if not isinstance(other, Matrix):
            return False
        if self.n != other.n or self.m != other.m:
            return False
        return all(self._a[i] == other._a[i] for i in range(self.n * self.m))
    
    def __ne__(self, other: "Matrix") -> bool:
        return not self.__eq__(other)
    
    def __repr__(self):
        string = []
        for i in range(self.n):
            string.append(f"{self._a[i*self.m: (i+1)*self.m]}")
        return "[" + '\n '.join(string) + "]"

    def inverse(self) -> "Matrix":
        """逆行列"""
        assert self.n == self.m, f"shape error: ({self.n},{self.m})"
        n = self.n
        a = self._a[:]
        b = [int(i==j) for i in range(n) for j in range(n)]

        for j in range(n):
            # 行の入れ替え
            if a[j*n+j] == 0:
                for i in range(j+1, n):
                    if a[i*n+j] != 0:
                        a[i*n: (i+1)*n], a[j*n: (j+1)*n] = a[j*n: (j+1)*n], a[i*n: (i+1)*n]
                        b[i*n: (i+1)*n], b[j*n: (j+1)*n] = b[j*n: (j+1)*n], b[i*n: (i+1)*n]
                        break
                else:
                    raise ValueError("inverse does not exist")
            
            # (j,j)を1にする
            inv = pow(a[j*n+j], Matrix.Mod-2, Matrix.Mod)
            for k in range(n):
                a[j*n+k] = a[j*n+k] * inv % Matrix.Mod
                b[j*n+k] = b[j*n+k] * inv % Matrix.Mod
            
            # ほかの行を0に
            for i in range(n):
                if i == j:
                    continue
                factor = a[i*n+j]
                for k in range(n):
                    a[i*n+k] = (a[i*n+k] - factor * a[j*n+k]) % Matrix.Mod
                    b[i*n+k] = (b[i*n+k] - factor * b[j*n+k]) % Matrix.Mod
            
        return Matrix._from_vector(b, n, n)

    def transpose(self) -> "Matrix":
        """転置行列"""
        data = [self[i,j] for j in range(self.m) for i in range(self.n)]
        return Matrix._from_vector(data, self.m, self.n)
    
    def swap_rows(self, i: int, j: int) -> None:
        """i行目とj行目を入れ替える"""
        assert 0 <= i < self.n and 0 <= j < self.n, f"i,j={i},{j} is index out of range"
        m = self.m
        self._a[i*m: (i+1)*m], self._a[j*m: (j+1)*m] = self._a[j*m: (j+1)*m], self._a[i*m: (i+1)*m]
    
    def multiply_row(self, i: int, k: int) -> None:
        """i行目をk倍する"""
        assert 0 <= i < self.n, f"i={i} is index out of range"
        for j in range(i*self.m, (i+1)*self.m):
            self._a[j] = self._a[j] * k % Matrix.Mod
    
    def add_row_multiple(self, i: int, j: int, k: int) -> None:
        """i行目にj行目のk倍を足す"""
        assert 0 <= i < self.n and 0 <= j < self.n, f"i,j={i},{j} is index out of range"
        for l in range(self.m):
            self._a[i*self.m+l] += k * self._a[j*self.m+l]
            self._a[i*self.m+l] %= Matrix.Mod
    
    def join_columns(self, other: "Matrix") -> "Matrix":
        """横に行列を結合"""
        assert self.n == other.n, f"shape error: ({self.n},{self.m}) and ({other.n},{other.m})"
        data = []
        for i in range(self.n):
            data.extend(self._a[i*self.m: (i+1)*self.m])
            data.extend(other._a[i*other.m: (i+1)*other.m])
        return Matrix._from_vector(data, self.n, self.m + other.m)
    
    def join_rows(self, other: "Matrix") -> "Matrix":
        """縦に行列を結合"""
        assert self.m == other.m, f"shape error: ({self.n},{self.m}) and ({other.n},{other.m})"
        data = self._a + other._a
        return Matrix._from_vector(data, self.n + other.n, self.m)
        
    @classmethod
    def _from_vector(cls, data: list, n: int, m: int) -> "Matrix":
        obj = cls.__new__(cls)
        obj.n = n
        obj.m = m
        obj._a = data
        return obj