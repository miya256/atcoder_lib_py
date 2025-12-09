from typing import Callable

class SparseTable:
    """
    冪等性が必要なのでmax,minとかはOK、sumとかはダメ
    """
    def __init__(self, op: Callable, data: list) -> None:
        # max,minであるindexがわかるために、indexも含めたopにしている
        self.op = lambda x, y: x if op(x[0], y[0]) == x[0] else y
        self.data = [[(v, i) for i, v in enumerate(data)]]
        for i in range(1, len(data).bit_length()):
            self.data.append([0] * (len(data)-(1<<i)+1))
            for j in range(len(data)-(1<<i)+1):
                self.data[i][j] = self.op(self.data[i-1][j], self.data[i-1][j+(1<<(i-1))])
    
    def prod(self, l: int, r: int) -> tuple[int, int]:
        """[l,r)までopした結果(値, index)"""
        assert 0 <= l <= r <= len(self.data), f"index error [l,r)=[{l},{r})"
        idx = (r-l).bit_length() - 1
        return self.op(self.data[idx][l], self.data[idx][r-(1<<idx)])