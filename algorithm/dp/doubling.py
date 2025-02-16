class Doubling:
    def __init__(self,k,trans):
        """
        n:状態数
        k:最大遷移回数
        dp:状態sから、2**i回遷移したあとの状態
        trans:状態sの次の状態の配列
        """
        self.n = len(trans)
        self.logk = k.bit_length()
        self.dp = [[0]*self.n for _ in range(self.logk)]

        for s in range(self.n):
            self.dp[0][s] = trans[s]
        for i in range(1,self.logk):
            for s in range(self.n):
                self.dp[i][s] = self.dp[i-1][self.dp[i-1][s]]
    
    def query(self,s,k):
        """状態sからk回遷移した後の状態を返す"""
        now = s
        for i in range(k.bit_length()):
            if k>>i & 1:
                now = self.dp[i][now]
        return now
