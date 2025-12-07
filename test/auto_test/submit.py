def edit_distance(s: str, t: str):
    """s, tの編集距離"""
    #sの先頭i文字目、tの先頭j文字目の編集距離
    dp = [[0 for _ in range(len(t)+1)] for _ in range(len(s)+1)]
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i+1][j+1] = min(dp[i][j+1]+1, dp[i+1][j]+1, dp[i][j])
            else:
                dp[i+1][j+1] = min(dp[i][j+1]+1, dp[i+1][j]+1, dp[i][j]+1)
    return dp[-1][-1]

m,n = map(int,input().split())
s = input()
t = input()
print(edit_distance(s,t))