def dist(a,b):
    return ((a[0]-b[0])*(a[0]-b[0]) + (a[1]-b[1])*(a[1]-b[1])) ** 0.5

n = int(input())
xy = [list(map(int,input().split())) for _ in range(n)]
inf = 1<<61
#訪れた集合がi、最後に訪れたのがj、の最小値
dp = [[inf]*n for _ in range(1<<n)]
dp[1][0] = 0 #始点は町1として問題ない

for i in range(1<<n):
    for j in range(n):
        if not i>>j&1: #最後に訪れたのがjなのに訪れてない場合は無視
            continue
        for k in range(n):
            if i>>k&1: #次にkを訪れるが、すでに訪れていたなら無視
                continue
            dp[i|1<<k][k] = min(dp[i|1<<k][k], dp[i][j]+dist(xy[j],xy[k]))

ans = inf
#最後に1に戻ってくる
for i in range(n):
    ans = min(ans,dp[-1][i]+dist(xy[0],xy[i]))
print(ans)