def edit_distance(s,t):
    #sの先頭i文字目、tの先頭j文字目の編集距離
    dp = [[0 for _ in range(len(t)+1)] for _ in range(len(s)+1)]
    for i in range(len(s)+1):
        for j in range(len(t)+1):
            if i > 0 and j > 0 and s[i-1] == t[j-1]:
                dp[i][j] = min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1])
            elif i > 0 and j > 0:
                dp[i][j] = min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+1)
            elif i > 0:
                dp[i][j] = dp[i-1][j]+1
            elif j > 0:
                dp[i][j] = dp[i][j-1]+1
    return dp[-1][-1]