def mat_mul(a,b,mod = None):
    res = [[0]*len(b[0]) for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                res[i][j] += a[i][k] * b[k][j]
            if mod:
                res[i][j] %= mod
    return res

def matPow(base,exp,mod = None):
    res = [[0]*len(base) for _ in range(len(base))]
    for i in range(len(base)):
        res[i][i] = 1
    while exp > 0:
        if exp & 1:
            res = mat_mul(base,res,mod)
        base = mat_mul(base,base,mod)
        exp >>= 1
    return res
