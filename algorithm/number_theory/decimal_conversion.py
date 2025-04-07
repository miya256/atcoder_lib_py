def convert_decimal(n,base):
    res = 0
    r = 1
    for i in range(len(n)):
        res += n[i] * r
        r *= base
    return res