#bitDPとかで高速化したいとき
#ゼータ変換はモノイドならok
#メビウス変換は元に戻す操作。ゼータ変換の逆演算があれば戻せる


def subset_zeta_transform(f: list[int], op: object = lambda x,y: x+y) -> list[int]:
    """部分集合の総積をとる(長さは2^n)"""
    assert len(f) & (len(f)-1) == 0, "長さは2の冪である必要があります"
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit:
                f[j] = op(f[j], f[j^bit])
    return f


def subset_mobius_transform(f: list[int], invop: object = lambda x,y: x-y) -> list[int]:
    """部分集合の総積を戻す(長さは2^n)"""
    assert len(f) & (len(f)-1) == 0, "長さは2の冪である必要があります"
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit:
                f[j] = invop(f[j], f[j^bit])
    return f


def superset_zeta_transform(f: list[int], op: object = lambda x,y: x+y) -> list[int]:
    """その要素をもつ集合の総積をとる(長さは2^n)"""
    assert len(f) & (len(f)-1) == 0, "長さは2の冪である必要があります"
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit == 0:
                f[j] = op(f[j], f[j|bit])
    return f


def superset_mobius_transform(f: list[int], invop: object = lambda x,y: x-y) -> list[int]:
    """その要素をもつ集合の総積を戻す(長さは2^n)"""
    assert len(f) & (len(f)-1) == 0, "長さは2の冪である必要があります"
    for i in range((len(f)-1).bit_length()):
        bit = 1 << i
        for j in range(len(f)):
            if j & bit == 0:
                f[j] = invop(f[j], f[j|bit])
    return f