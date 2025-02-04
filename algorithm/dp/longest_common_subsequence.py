def lcs(s,t,isRestored=False):
    dp = [[0]*(len(t)+1) for _ in range(len(s)+1)]
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1],dp[i+1][j])
    if not isRestored:
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
        else:#i文字目とj文字目が違うなら、長さが変わらなほうへ移動
            if dp[i+1][j+1] == dp[i][j+1]:
                i -= 1
            else:
                j -= 1
    return ''.join(string[::-1])

#片方が順列ならば、ラベルを付け替えることでLISを求める問題に帰着できる
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

def lcs(a,b):
    na = [0] * len(a)
    for i in range(len(a)):
        na[a[i]] = i
    nb = []
    for i in range(len(b)):
        nb.append(na[b[i]])
    return lis(nb)