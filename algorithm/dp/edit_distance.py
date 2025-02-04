inf = 1<<61
def edit_distance(s,t):
    #sの先頭i文字目、tの先頭j文字目の編集距離
    dp = [[inf for _ in range(len(t)+1)] for _ in range(len(s)+1)]
    dp[0][0] = 0
    for i in range(len(s)):
        for j in range(len(t)):
            dp[i+1][j+1] = min(dp[i][j+1]+1,dp[i+1][j]+1,dp[i][j]+(0 if s[i] == t[j] else 1))
    return dp[-1][-1]
