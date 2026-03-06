#n人を区別のあるちょうどk個のグループに分ける場合の数
def surjections(n,k):
    res = 0
    sign = (-1) ** ((k-1)&1)
    comb = k
    for i in range(1,k+1):
        res += sign * comb * pow(i,n)
        sign *= -1
        comb = comb * (k-i) // (i+1)
    return res

#n人を区別のないちょうどk個のグループに分ける場合の数
def stirling(n,k):
    if k == 1 or n == k:
        return 1
    return stirling(n-1,k-1) + k * stirling(n-1,k)

#n人を区別のないk個以下のグループに分ける場合の数
def bell(n,k):
    res = 0
    for i in range(1,k+1):
        res += stirling(n,i)
    return res