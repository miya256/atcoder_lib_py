#巡回セールスマン(一周して戻ってくる最短経路)

inf = 1<<61
def tsp(n):
    #すでに訪れた集合がs、最後に訪れたのがi、の最小値
    dp = [[inf]*n for _ in range(1<<n)]
    dp[1][0] = 0 #1周するなら、始点は点0としてよい

    for s in range(1<<n):
        for i in range(n): #i->jへ遷移
            if not s>>i&1: #iに訪れてないことになってたら無視
                continue
            for j in range(n):
                if s>>j&1: #jをすでに訪れていることになってたら無視
                    continue
                dp[s|1<<j][j] = min(dp[s|1<<j][j], dp[s][i] + "i->jの距離")
    ans = inf
    for i in range(n): #最後に0にもどる
        ans = min(ans, dp[-1][i]+"i->0の距離")
    return ans

