class Ring:
    def __init__(self,n):
        """周期nで 0~n-1"""
        self.n = n
    
    def forward_cost(self,start,end):
        """数字が増える方向に進んだ場合の道のり"""
        return (end - start) % self.n
    
    def backward_cost(self,start,end):
        """逆方向の道のり"""
        return (start - end) % self.n
    
    def isbetween(self,start,end,val):
        """
        数字が増える方向のstartからendまでの間に、valが存在するか
        =をつけるとstartとendも含める
        """
        return (val-start) * (start-end) * (end - val) < 0