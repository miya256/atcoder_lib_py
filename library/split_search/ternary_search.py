from typing import Callable


def ternary_search(l: float, r: float, f: Callable) -> float:
    """
    三分探索
    狭義の単調性が必要
    """
    while r - l > 1e-9:
        ml = (l * 2 + r) / 3
        mr = (l + r * 2) / 3
        if f(ml) > f(mr):
            l = ml
        else:
            r = mr
    return l
