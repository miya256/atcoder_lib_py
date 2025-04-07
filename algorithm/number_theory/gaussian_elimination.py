#GaussianEliminationやRowReductionなどと呼ばれている
#O(R*C^2)
#xorの場合はmod 2でやればいい
def gaussian_elimination(a,mod,extend=False): #Ax=bのとき、bの列はやらないからextendで場合分け
    n,m = len(a),len(a[0])
    rank = 0
    for j in range(m):
        if extend and j == m-1:
            return rank
        pivot = -1 #列jの非ゼロの要素を探す
        for i in range(rank,n):
            if a[i][j] != 0:
                pivot = i
                break
        else:
            continue
        a[rank],a[pivot] = a[pivot],a[rank] #swapしているが無理だったら、1つずつやろう
        inv = pow(a[rank][j],mod-2,mod)
        for k in range(j,m): #a[rank][j]で割って、a[rank][j]を1に
            a[rank][k] = a[rank][k] * inv % mod
        for i in range(n): #j列目のrank行目以外を0に
            if i != rank and a[i][j]:
                for k in range(m-1,j-1,-1): #a[i][j]倍するから後ろからやってる。前からやるとa[i][j]=0になって、0倍になるから
                    a[i][k] = (a[i][k] - a[rank][k] * a[i][j]) % mod
        rank += 1
    return rank

def linear_equation(a,b,mod):
    n,m = len(a),len(a[0])
    for i in range(n):
        a[i].append(b[i])
    rank = gaussian_elimination(a,mod,True)
    for i in range(rank,n):
        if a[i][m] != 0: #変数の係数がすべて0になっているのに、定数部分が0でなかったら解なし
            return None

    res = [[]] #解 x = a0 + c1a1 + c2a2 + ... aは基底,cは未定定数。i行目にベクトルaiが入る
    const = [] #未定定数になるXiのiを入れる
    i = 0
    for j in range(m):
        if i < n and a[i][j] == 1:
            res[0].append(a[i][m])
            i += 1
        else:
            const.append(j)
            res[0].append(0)

    res += [[] for _ in range(len(const))]
    i = 0
    for j in range(m):
        if i < n and a[i][j] == 1:
            for idx,k in enumerate(const,1):
                res[idx].append((-a[i][k]) % mod)
            i += 1
        else:
            for idx,k in enumerate(const,1):
                res[idx].append(1 if k == j else 0)
    #解を1つ求めるならres[0]が答え
    #他の解は、resの0行目以外の行を定数倍して、列ごとに足したものが答え
    return res