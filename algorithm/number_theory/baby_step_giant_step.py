#f^n(x) = yとなる最小のn
#f^(im+j)(x) = y
#f^im(x) = f^-j(y)
def baby_step_giant_step(x,y,p): #x^n = y (mod p)となる最小のn
    m = int(p**0.5)
    ix  = pow(x,p-2,p)
    j = {} #yx^-j:j
    right = y #右辺
    for i in range(m):
        if right not in j:
            j[right] = i
        right = (right * ix) % p
    xm = pow(x,m,p)
    left = 1
    for i in range(m+1):
        if left in j:
            return i*m+j[left]
        left = (left * xm) % p
    return -1 #存在しない


#ABC270G--------------------------------------------
def mapping_pow(f,m,mod): #f = [a,b] = ax+b
    id = [1,0]
    while m:
        if m & 1:
            id = [(id[0]*f[0]) % mod, (id[0]*f[1]+id[1]) % mod]
        f = [(f[0]*f[0]) % mod, (f[0]*f[1]+f[1]) % mod]
        m >>= 1
    return id

def baby_step_giant_step(f_m,f_inv,f0,y,m, p):
    j = {}
    right = y
    for i in range(m):
        if right not in j:
            j[right] = i
        right = (f_inv[0] * right + f_inv[1]) % p #f_inv(right)
    left = f0
    for i in range(p//m+1):
        if left in j:
            return i*m+j[left]
        left = (f_m[0] * left + f_m[1]) % p #f_m(left)
    return -1

def solve():
    p,a,b,s,g = map(int,input().split())
    if a==0: #a = 0のとき、逆関数は存在しないので場合分け。
        print(0 if s == g else 1 if b == g else -1)
        return
    m = int(p**0.5)
    f_m = mapping_pow([a,b],m,p)
    f_inv = [pow(a,p-2,p),(-pow(a,p-2,p)*b)%p] #y=ax+b -> a^-1y - ba^-1
    print(baby_step_giant_step(f_m,f_inv,s,g,m,p))

for _ in range(int(input())):
    solve()
