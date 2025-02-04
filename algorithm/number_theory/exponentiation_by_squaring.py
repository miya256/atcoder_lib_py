def pow(base,exp,mod = None):
    res=1
    while exp > 0:
        if exp & 1:
            if mod is None:
                res *= base
            else:
                res = res * base % mod
        if mod is None:
            base *= base
        else:
            base = base * base % mod
        exp >>= 1
    return res