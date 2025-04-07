def extgcd(m,n):
    if n == 0:
        return m,1,0
    gcd,s,t = extgcd(n,m%n)
    return gcd, t, s-(m//n)*t

def indefinite_equation(a, b, c):
    """ax+by=c の解"""
    gcd,x,y = extgcd(a,b) #c=gcd(a,b)の場合の解を求めて
    if c % gcd != 0:
        return None,None
    x *= c // gcd
    y *= c // gcd
    return x, y

def inv(n,mod):
    x,_ = indefinite_equation(n,mod,1)
    return x