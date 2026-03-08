def quick_sort(a):
    if len(a) <= 1:
        return a
    pl, pr = 0, len(a)
    while pr - pl > 1:
        if a[pl] > a[pl+1]:
            a[pl],a[pl+1] = a[pl+1],a[pl]
            pl += 1
        else:
            a[pl+1],a[pr-1] = a[pr-1],a[pl+1]
            pr -= 1
    a[:pl] = quick_sort(a[:pl])
    a[pr:] = quick_sort(a[pr:])
    return a