class Accumulate:
    """
    Attributes:
        shape: 元の配列の形状 例: [1, m, n]
        stride: 累積和配列の各次元の倍率 例: [1, m+1, (n+1)*(m+1)]
    """

    def __init__(self, a: list) -> None:
        self._shape = self._build_shape(a)
        self._stride = self._build_stride(self._shape)
        self._acc: list[int] = self._build_acc(a, self._shape, self._stride)

    def _build_shape(self, a: list) -> list[int]:
        shape = []
        while isinstance(a, list):
            shape.append(len(a))
            a = a[0]
        shape.append(1)
        return shape[::-1]

    def _build_stride(self, shape: list[int]) -> list[int]:
        stride = shape[:]
        for i in range(self.dim):
            stride[i + 1] = (stride[i + 1] + 1) * stride[i]
        return stride

    def _build_acc(self, a: list, shape: list[int], stride: list[int]) -> list[int]:
        acc = []
        stack = [(a, -2)]
        while stack:
            a, i = stack.pop()
            if isinstance(a, int):
                acc.append(a)
                continue
            acc.extend([0] * stride[i])
            for ai in a[::-1]:
                stack.append((ai, i - 1))

        for k in range(self.dim):
            for i in range(len(acc)):
                c = stride[k]
                d = shape[k + 1] + 1
                if (i + c) // c % d == 0:
                    continue
                acc[i + c] += acc[i]
        return acc

    def sum(self, l: list[int], r: list[int]) -> int:
        """[l, r) の和"""
        assert len(l) == len(r) == self.dim
        s = 0
        for b in range(1 << self.dim):
            i = 0
            sign = -1 if b.bit_count() % 2 else 1
            for d in range(self.dim):
                i += (l[d] if b >> d & 1 else r[d]) * self._stride[-d - 2]
            s += sign * self._acc[i]
        return s

    @property
    def dim(self) -> int:
        return len(self._shape) - 1
