def quotient_range(n: int) -> list[tuple[int, int, int]]:
    """
    floor(n/i)=k となるiの範囲[l,r)の一覧
    [(l, r, k), ...]
    """
    res = []
    i = 1
    while i <= n:
        q = n // i
        j = n // q + 1
        res.append((i, j, q))
        i = j
    return res
