def merge_sort(a):
    if len(a) <= 1:
        return a
    l = merge_sort(a[:len(a)//2])
    r = merge_sort(a[len(a)//2:])
    a = []
    while l and r:
        if l[-1] > r[-1]:
            a.append(l.pop())
        else:
            a.append(r.pop())
    a += l[::-1] + r[::-1]
    return a[::-1]
