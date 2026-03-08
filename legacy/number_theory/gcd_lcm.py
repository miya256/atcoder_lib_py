def gcd(m,n):
    return m if n == 0 else gcd(n,m%n)

def lcm(m,n):
    g = gcd(m,n)
    return m*n//g

m,n = map(int,input().split())
print(gcd(m,n))
print(lcm(m,n))
