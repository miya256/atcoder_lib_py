def convertRadix(n, radix):
    """res[0]が下位桁"""
    negative = (radix < 0)
    radix = abs(radix)
    res = []
    while n:
        res.append(n % radix)
        n //= radix
        if negative:
            n = -n
    return res