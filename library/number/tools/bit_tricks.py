x=0

x & -x    # 右端の1だけ残す
x & (x-1) # 右端の1を消す
~x        # bit反転


def f(s): #sの部分集合全列挙
    #0含めない
    t = (s-1)&s
    while t > 0:
        f(t)+f(s^t)
        t -= 1
        t &= s