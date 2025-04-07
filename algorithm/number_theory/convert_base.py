def convert_base(n, base):
    """res[0]が下位桁。baseが負でもok"""
    negative = (base < 0)
    base = abs(base)
    res = []
    while n:
        res.append(n % base)
        n //= base
        if negative:
            n = -n
    return res