#startとvalが同じところにあるときとかも考えたほうがいいかも
class Ring:
    def __init__(self,n):
        """
        周期nで 0~n-1
        forward: 数字が増える方向
        backward: 数字が減る方向
        """
        self.n = n
    
    def _mod(self,*val):
        return map(lambda x:int(x)%self.n, val)
    
    def forward_cost(self,start,end):
        """forwardに進んだ場合の道のり"""
        return (end - start) % self.n
    
    def backward_cost(self,start,end):
        """backwardに進んだ場合の道のり"""
        return (start - end) % self.n
    
    def on_forward_path(self,start,end,point):
        """
        forwardのstartからendまでの間にpointが存在するか
        =をつけるとstartとendも含める
        """
        start,end,point = self._mod(start,end,point)
        return (point-start) * (start-end) * (end - point) < 0
    
    def on_backward_path(self,start,end,point):
        """backwardのstartからendまでの間にpointが存在するか"""
        start,end,point = self._mod(start,end,point)
        return (point-start) * (start-end) * (end - point) > 0
    
    def via_cost(self,start,end,point):
        """startからendまで、pointを通るほうのコスト"""
        return self.forward_cost(start,end) if self.on_forward_path(start,end,point) else self.backward_cost(start,end)
    
    def avoid_cost(self,start,end,point):
        """startからendまで、pointを避けるほうのコスト"""
        return self.forward_cost(start,end) if self.on_backward_path(start,end,point) else self.backward_cost(start,end)
    
    def mid_point(self, a, b):
        """a,bの中点(2つ)を返す。(n,a,b)=(3,1,2) -> 1.5, 0"""
        p1 = ((a + b) / 2) % self.n
        p2 = ((a + b + self.n) / 2) % self.n
        return p1, p2
        
