from bisect import bisect_left, bisect_right

def lis(a: list[int]) -> int:
    """aの最長増加部分列"""
    dp = []
    for v in a:
        idx = bisect_left(dp, v)
        if idx < len(dp):
            dp[idx] = v
        else:
            dp.append(v)
    return len(dp)
