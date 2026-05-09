def gcd(*nums: int) -> int:
    g = 0
    for x in nums:
        m, n = g, x
        while n != 0:
            m, n = n, m % n
        g = m
    return abs(g)


def lcm(*nums: int, limit: int | None = None) -> int:
    l = 1
    for x in nums:
        if x == 0:
            return 0
        g = gcd(l, x)
        if limit is not None and l // g > limit // x:
            return limit + 1
        l = l // g * x
    return abs(l)
