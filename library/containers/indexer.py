from typing import Callable


def make_indexer(
    shape: tuple[int, ...],
) -> tuple[Callable[..., int], Callable[[int], tuple[int, ...]]]:
    dim = len(shape)
    stride = [1] * dim
    for i in range(dim - 1, 0, -1):
        stride[i - 1] = stride[i] * shape[i]

    if dim == 1:
        return lambda i0: i0, lambda i: (i,)
    if dim == 2:
        s0, s1 = stride
        return lambda i0, i1: i0 * s0 + i1 * s1, lambda i: (i // s0, i % s0 // s1)
    if dim == 3:
        s0, s1, s2 = stride
        return (
            lambda i0, i1, i2: i0 * s0 + i1 * s1 + i2 * s2,
            lambda i: (i // s0, i % s0 // s1, i % s1 // s2),
        )
    if dim == 4:
        s0, s1, s2, s3 = stride
        return (
            lambda i0, i1, i2, i3: i0 * s0 + i1 * s1 + i2 * s2 + i3 * s3,
            lambda i: (i // s0, i % s0 // s1, i % s1 // s2, i % s2 // s3),
        )

    def flat(*indices) -> int:
        assert len(indices) == dim
        return sum(i * s for i, s in zip(indices, stride))

    def unflat(i) -> tuple[int, ...]:
        indices = []
        for s in stride:
            indices.append(i // s)
            i %= s
        return tuple(indices)

    return flat, unflat
