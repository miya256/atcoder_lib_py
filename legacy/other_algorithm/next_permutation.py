def next_permutation(p):
    for i in range(len(p)-1,0,-1):
        if p[i-1] < p[i]:
            idx = -1 #p[i-1]より大きい最小の値のindex
            for j in range(i,len(p)):
                if p[j] > p[i-1]:
                    idx = j
            p[i-1],p[idx] = p[idx],p[i-1]
            return p[:i-1]+[p[i-1]]+p[i:][::-1]
    return False

p = [1,2,3,4,5]
while p:
    print(p)
    p = next_permutation(p)