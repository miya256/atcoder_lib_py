def edit_distance(s: str, t: str):
    """s, tの編集距離(挿入、削除、変更)"""
    inf = 1<<61
    #sの先頭i文字、tの先頭j文字の編集距離
    dp = [[inf for _ in range(len(t)+1)] for _ in range(len(s)+1)]
    for i in range(len(s)+1):
        dp[i][0] = i
    for j in range(len(t)+1):
        dp[0][j] = j
    
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i+1][j+1] = min(dp[i][j+1]+1, dp[i+1][j]+1, dp[i][j])
            else:
                # 変更禁止の場合は、右だけ+2にする
                dp[i+1][j+1] = min(dp[i][j+1]+1, dp[i+1][j]+1, dp[i][j]+1)
    return dp[-1][-1]