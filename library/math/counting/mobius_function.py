class Mobius:
    """
    メビウス関数
    2乗で割れる : 0
    因数の数が奇数個 : -1
    因数の数が偶数個 : +1
    """
    def __init__(self, n: int) -> None:
        self.n = n
        self._mobius = self._build(n)
    
    def _build(self, n: int) -> list[int]:
        mobius = [1] * (n+1)
        is_prime = [True] * (n+1)
        is_prime[1] = False
        for i in range(2, n+1):
            if is_prime[i]:
                mobius[i] = -1
                for j in range(i*2, n+1, i):
                    is_prime[j] = False
                    if j % (i * i) == 0:
                        mobius[j] = 0
                    else:
                        mobius[j] = -mobius[j]
        return mobius
    
    def __call__(self, n: int) -> int:
        return self._mobius[n]
    
    def mobius(self, n: int) -> int:
        return self._mobius[n]