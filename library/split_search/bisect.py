def bisect_left(a: list, x, key=None) -> int:
    l, r = -1, len(a)
    while r-l > 1:
        mid = (l+r)//2
        if (key is None and a[mid] < x) or (key(a[mid]) < key(x)):
            l = mid
        else:
            r = mid
    return r

def bisect_right(a: list, x, key=None) -> int:
    l, r = -1, len(a)
    while r-l > 1:
        mid = (l+r)//2
        if (key is None and a[mid] <= x) or (key(a[mid]) <= key(x)):
            l = mid
        else:
            r = mid
    return r