from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class SparseTable(Generic[T]):
    """
    冪等性が必要なのでmax,minとかはOK、sumとかはダメ
    """

    def __init__(self, op: Callable[[T, T], T], data: list) -> None:
        # max,minであるindexがわかるために、indexも含めたopにしている
        self.op = lambda x, y: x if op(x[0], y[0]) == x[0] else y
        self.data: list[list[tuple[T, int]]] = [[(v, i) for i, v in enumerate(data)]]

        pdata: list[tuple[T, int]] = self.data[0]
        for i in range(1, len(data).bit_length()):
            ndata: list[tuple[T, int]] = []
            for j in range(len(data) - (1 << i) + 1):
                ndata.append(self.op(pdata[j], pdata[j + (1 << (i - 1))]))
            self.data.append(ndata)
            pdata = ndata

    def prod(self, l: int, r: int) -> tuple[T, int]:
        """[l,r)までopした結果(値, その値になる最小のindex)"""
        orig_l = l
        orig_r = r
        l += len(self.data[0]) if l < 0 else 0
        r += len(self.data[0]) if r < 0 else 0
        assert 0 <= l <= r <= len(self.data[0]), (
            f"invalid range: [l,r)=[{orig_l},{orig_r})->[{l},{r})"
        )

        idx = (r - l).bit_length() - 1
        return self.op(self.data[idx][l], self.data[idx][r - (1 << idx)])
