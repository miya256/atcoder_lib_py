import random
def primitive_root(p: int) -> int:
    """素数pの原子根"""
    #p-1の素因数を抽出
    prime_factor = [2]
    tmp = p-1
    while tmp % 2 == 0:
        tmp //= 2
    k = 3
    while k*k <= tmp:
        if tmp % k == 0:
            prime_factor.append(k)
            while tmp % k == 0:
                tmp //= k
        k += 2
    if tmp > 1:
        prime_factor.append(tmp)
    
    while True:
        g = random.randint(2,p-1)
        if all(pow(g,(p-1)//i,p) != 1 for i in prime_factor):
            return g

    