class Accumulation:
    """
    Attributes:
        shape : padding後配列の形状 例: [H+2, W+2, D+2]
        stride: padding後配列の各次元の倍率 例: [(W+2)*(D+2), D+2, 1]
    """

    def __init__(self, a: list) -> None:
        self._shape = self._build_shape(a)
        self._stride = self._build_stride(self._shape)
        self._acc: list[int] = self._build_acc(a, self._stride)

    def _build_shape(self, a: list) -> tuple[int, ...]:
        shape = []
        while isinstance(a, list):
            shape.append(len(a) + 2)
            a = a[0]
        return tuple(shape)

    def _build_stride(self, shape: tuple[int, ...]) -> tuple[int, ...]:
        stride = [1] * self.dim
        for i in range(self.dim - 2, -1, -1):
            stride[i] = stride[i + 1] * shape[i + 1]
        return tuple(stride)

    def _build_acc(self, a: list, stride: tuple[int, ...]) -> list[int]:
        acc = []
        stack: list[tuple[list | int | None, int]] = [(a, 0)]
        while stack:
            v, i = stack.pop()
            if v is None:
                acc.extend([0] * stride[i])
                continue
            if isinstance(v, int):
                acc.append(v)
                continue
            acc.extend([0] * stride[i])
            stack.append((None, i))
            for vi in v[::-1]:
                stack.append((vi, i + 1))
        return acc

    def _print_str(self, data, dim) -> str:
        if dim == 1:
            return str(data)
        string = ["["]
        for i in range(self._shape[-dim]):
            string.append(
                self._print_str(
                    data[i * self._stride[-dim] : (i + 1) * self._stride[-dim]], dim - 1
                )
            )
            string.append("\n" + " " * (self.dim - dim + (i != self._shape[-dim] - 1)))
        string.append("]")
        return "".join(string)

    def __repr__(self) -> str:
        orig_shape = tuple(d - 2 for d in self._shape)
        shape_info = f"shape: {orig_shape} - padding -> {self._shape}"
        context = self._print_str(self._acc, self.dim)
        return f"Accumulation (\n{shape_info}\n{context}\n)"

    def accumulate(self) -> None:
        for k in range(self.dim):
            c = self._stride[k]
            d = self._shape[k]
            for i in range(len(self._acc)):
                if (i + c) // c % d == 0:
                    continue
                self._acc[i + c] += self._acc[i]

    def get(self, indices: tuple[int, ...]) -> int:
        assert len(indices) == self.dim, (
            f"expected {self.dim} indices, got {len(indices)}"
        )
        return self._acc[self._index(indices)]

    def set(self, indices: tuple[int, ...], x: int) -> None:
        assert len(indices) == self.dim, (
            f"expected {self.dim} indices, got {len(indices)}"
        )
        self._acc[self._index(indices)] = x

    def add(self, indices: tuple[int, ...], x: int) -> None:
        assert len(indices) == self.dim, (
            f"expected {self.dim} indices, got {len(indices)}"
        )
        self._acc[self._index(indices)] += x

    def range_add(self, l: tuple[int, ...], r: tuple[int, ...], f: int) -> None:
        """[l, r) にfを加える"""
        assert len(l) == len(r) == self.dim, (
            f"expected {self.dim} indices, got {len(l)} for l and {len(r)} for r"
        )
        assert all(0 <= li <= ri <= si - 2 for li, ri, si in zip(l, r, self._shape)), (
            f"invalid range: [l,r)=[{l},{r})"
        )
        for b in range(1 << self.dim):
            i = 0
            sign = -1 if b.bit_count() % 2 else 1
            for d in range(self.dim):
                i += (r[d] + 1 if b >> d & 1 else l[d] + 1) * self._stride[d]
            self._acc[i] += sign * f

    def sum(self, l: tuple[int, ...], r: tuple[int, ...]) -> int:
        """[l, r) の和"""
        assert len(l) == len(r) == self.dim, (
            f"expected {self.dim} indices, got {len(l)} for l and {len(r)} for r"
        )
        assert all(0 <= li <= ri <= si - 2 for li, ri, si in zip(l, r, self._shape)), (
            f"invalid range: [l,r)=[{l},{r})"
        )
        s = 0
        for b in range(1 << self.dim):
            i = 0
            sign = -1 if b.bit_count() % 2 else 1
            for d in range(self.dim):
                i += (l[d] if b >> d & 1 else r[d]) * self._stride[d]
            s += sign * self._acc[i]
        return s

    def _index(self, indices: tuple[int, ...]) -> int:
        return sum(i * s for i, s in zip(indices, self._stride))

    @property
    def dim(self) -> int:
        return len(self._shape)
