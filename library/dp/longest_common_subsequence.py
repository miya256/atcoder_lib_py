def lcs(s: str, t: str, is_restored: bool = False) -> int|str:
    """s,tの最長共通部分列"""
    dp = [[0]*(len(t)+1) for _ in range(len(s)+1)]
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    if not is_restored:
        return dp[-1][-1]
    
    #復元
    string = []
    i = len(s)-1
    j = len(t)-1
    while len(string) < dp[-1][-1]:
        if s[i] == t[j]:
            string.append(s[i])
            i -= 1
            j -= 1
        else: # i文字目とj文字目が違うなら、長さが変わらなほうへ移動
            if dp[i+1][j+1] == dp[i][j+1]:
                i -= 1
            else:
                j -= 1
    return ''.join(string[::-1])