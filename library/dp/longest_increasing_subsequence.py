from bisect import bisect_left


def lis(a: list[int]) -> list[int]:
    """
    aの最長増加部分列を一つ求める
    添え字のリストを返す
    """
    dp_v = []
    dp_i = []
    prev_i = [-1] * len(a)
    for i, v in enumerate(a):
        idx = bisect_left(dp_v, v)
        if idx < len(dp_v):
            dp_v[idx] = v
            dp_i[idx] = i
        else:
            dp_v.append(v)
            dp_i.append(i)
        if idx > 0:
            prev_i[i] = dp_i[idx - 1]

    # 復元
    res = []
    k = dp_i[-1]
    while k != -1:
        res.append(k)
        k = prev_i[k]
    return res[::-1]
