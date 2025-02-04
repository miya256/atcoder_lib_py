def zAlgorithm(s):
    """sとs[i:]のLCPの長さ"""
    z = [0]*len(s)
    z[0] = len(s)
    l = r = 0
    for i in range(1,len(s)):
        if z[i-l] < r-i:
            z[i] = z[i-l]
            continue
        r = max(r,i)
        while r < len(s) and s[r] == s[r-i]:
            r += 1
        z[i] = r-i
        l = i
    return z
