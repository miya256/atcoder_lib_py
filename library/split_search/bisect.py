from typing import Callable


def bisect_left(a: list, x, key: Callable = lambda x: x) -> int:
    l, r = -1, len(a)
    while r - l > 1:
        mid = (l + r) // 2
        if key(a[mid]) < key(x):
            l = mid
        else:
            r = mid
    return r


def bisect_right(a: list, x, key: Callable = lambda x: x) -> int:
    l, r = -1, len(a)
    while r - l > 1:
        mid = (l + r) // 2
        if key(a[mid]) <= key(x):
            l = mid
        else:
            r = mid
    return r
