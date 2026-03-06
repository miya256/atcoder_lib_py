import bisect
def lis(a):
    dp = []
    for v in a:
        idx = bisect.bisect_left(dp,v)
        if idx < len(dp):
            dp[idx] = v
        else:
            dp.append(v)
    return len(dp)
