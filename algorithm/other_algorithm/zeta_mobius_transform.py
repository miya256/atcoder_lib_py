def zeta_transform(f):
    """部分集合の総和(長さは2^n)"""
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit:
                f[j] += f[j^bit]
    return f

def mobius_transform(f):
    """部分集合の総和(長さは2^n)"""
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit:
                f[j] -= f[j^bit]
    return f

def zeta_transform(f):
    """その要素をもつ集合の和(長さは2^n)"""
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit == 0:
                f[j] += f[j|bit]
    return f

def mobius_transform(f):
    """その要素をもつ集合の和(長さは2^n)"""
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit == 0:
                f[j] -= f[j|bit]
    return f