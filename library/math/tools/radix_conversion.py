def convert_radix(n: int, radix: int) -> list[int]:
    """
    nをradix進数にする
    radixが負でもok
    res[i] が radix ^ i の位
    """
    assert abs(radix) > 1
    if n == 0:
        return [0]
    is_neg_radix = (radix < 0)
    radix = abs(radix)
    res = []
    while n:
        res.append(n % radix)
        n //= radix
        if is_neg_radix:
            n = -n
    return res


def to_decimal(digits: list[int], radix: int) -> int:
    """convert radixしたやつを戻す"""
    res = 0
    r = 1
    for digit in digits:
        res += digit * r
        r *= radix
    return res