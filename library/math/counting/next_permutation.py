def next_permutation(p: list) -> bool:
    """pの次の順列 in-place"""
    for i in range(len(p)-1, 0, -1):
        if p[i-1] < p[i]:
            for j in range(len(p)-1, i-1, -1):
                if p[j] > p[i-1]: #p[i-1]より大きい最小の値のindex
                    p[i-1], p[j] = p[j], p[i-1]
                    break
            p[i:] = reversed(p[i:])
            return True
    return False