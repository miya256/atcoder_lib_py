class Doubling:
    """
    ダブリング

    Attributes:
        n   : 状態数
        k   : 最大遷移回数
        dp  : 状態sから 2^i 回遷移したあとの状態
        next: 次の状態の配列
    
    Methods:
        jump(s,k): 状態sからk回遷移した後の状態を返す
    """
    def __init__(self, k: int, next: list[int]) -> None:
        self._n = len(next)
        self._logk = k.bit_length()
        self._dp = self._build(next)
    
    def _build(self, next: list[int]) -> list[list[int]]:
        dp = [next] + [[-1]*self._n for _ in range(self._logk)]
        for i in range(1, self._logk):
            for s in range(self._n):
                dp[i][s] = dp[i-1][dp[i-1][s]]
        return dp
    
    def jump(self, s: int, k: int) -> int:
        """状態sからk回遷移した後の状態を返す"""
        for i in range(k.bit_length()):
            if k >> i & 1:
                s = self._dp[i][s]
        return s
