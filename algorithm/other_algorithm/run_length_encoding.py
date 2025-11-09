def run_length_encoding(a):
    rle = []
    l = r = 0
    while l < len(a):
        while r < len(a) and a[l] == a[r]:
            r += 1
        rle.append((a[l], r-l))
        l = r
    return rle