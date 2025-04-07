def binary_search(ok,ng,*args):
    def satisfies(x,*args):
        """xのとき条件を満たすか"""
        return
    
    ng += 1 if ok < ng else -1
    while abs(ok-ng) > 1:
        mid = (ok+ng)//2
        if satisfies(mid,*args):
            ok = mid
        else:
            ng = mid
    return ok


def bisect_left(a,x):
    l,r = -1,len(a)
    while r-l > 1:
        mid = (l+r)//2
        if a[mid] < x:
            l = mid
        else:
            r = mid
    return r

def bisect_right(a,x):
    l,r = -1,len(a)
    while r-l > 1:
        mid = (l+r)//2
        if a[mid] <= x:
            l = mid
        else:
            r = mid
    return r