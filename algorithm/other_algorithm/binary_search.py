def binary_search():
    l,r = 0,n
    while r-l > 1:
        mid = (l+r)//2
        if isok():
            l = mid
        else:
            r = mid

def bisect_left(a,x):
    l,r = 0,len(a)
    while l != r:
        mid = (l+r)//2
        if a[mid] < x:
            l = mid+1
        else:
            r = mid
    return l

def bisect_right(a,x):
    l,r = 0,len(a)
    while l != r:
        mid = (l+r)//2
        if a[mid] <= x:
            l = mid+1
        else:
            r = mid
    return l