def pow(radix: int, exp: int, mod: int | None = None) -> int:
    res = 1
    while exp > 0:
        if exp & 1:
            res *= radix
        radix *= radix
        exp >>= 1

        if mod is not None:
            res %= mod
            radix %= mod
    return res