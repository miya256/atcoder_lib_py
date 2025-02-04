def convertDecimal(n,radix):
    res = 0
    r = 1
    for i in range(len(n)):
        res += n[i] * r
        r *= radix
    return res