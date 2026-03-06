def solve_integer_linear(a: int, b: int, c: int) -> tuple[int, int, int] | None:
    """
    ax+by=c の解

    解の1つを(x0,y0), gcd(a,b)=dとおくと、
    x = ak/d + x0
    y = -bk/d + y0

    n の mod を法とする逆元は、eq(n, mod, 1) の x
    """
    def extgcd(m: int, n: int) -> tuple[int, int, int]:
        if n == 0:
            return m , 1, 0
        gcd, s, t = extgcd(n, m % n)
        return gcd, t, s - (m // n) * t
    
    gcd, x, y = extgcd(a,b) # c=gcd(a,b)の場合の解を求めて
    if c % gcd != 0:
        return None # 解なし
    x *= c // gcd
    y *= c // gcd
    return x, y, gcd