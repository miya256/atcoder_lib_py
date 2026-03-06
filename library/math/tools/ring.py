class Ring:
    """
    円環上の道のりを計算する
    周期nで 0~n-1
    forward  : 数字が増える方向
    backward : 数字が減る方向

    Methods:
        forward_cost     : forwardに進んだ場合の道のり
        backward_cost    : backwardに進んだ場合の道のり
        via_cost         : startからendまで、pointを通るほうのコスト
        avoid_cost       : startからendまで、pointを避けるほうのコスト
        on_forward_path  : forwardのstartからendまでの間にpointが存在するか
        on_backward_path : backwardのstartからendまでの間にpointが存在するか
        mid_point        : a,bの中点(2つ)を返す。(n,a,b)=(3,1,2) -> 1.5, 0
    """
    def __init__(self, n: int) -> None:
        self.n = n
    
    def forward_cost(self, start: int, end: int) -> int:
        """forwardに進んだ場合の道のり"""
        return (end - start) % self.n
    
    def backward_cost(self, start: int, end: int) -> int:
        """backwardに進んだ場合の道のり"""
        return (start - end) % self.n
    
    def via_cost(self, start: int, end: int, point: int) -> int:
        """startからendまで、pointを通るほうのコスト"""
        if self.on_forward_path(start, end, point):
            return self.forward_cost(start, end)
        return self.backward_cost(start, end)
    
    def avoid_cost(self, start: int, end: int, point: int) -> int:
        """startからendまで、pointを避けるほうのコスト"""
        if self.on_backward_path(start, end, point):
            return self.forward_cost(start, end)
        return self.backward_cost(start, end)
    
    def on_forward_path(self, start: int, end: int, point: int, inclusive: bool = False) -> bool:
        """forwardのstartからendまでの間にpointが存在するか"""
        start, end, point = self._mod(start, end, point)
        if inclusive: #start と end も含めるなら
            return (point - start) * (start - end) * (end - point) <= 0
        return (point - start) * (start - end) * (end - point) < 0
    
    def on_backward_path(self, start: int, end: int, point: int, inclusive: bool = False) -> bool:
        """backwardのstartからendまでの間にpointが存在するか"""
        start, end, point = self._mod(start, end, point)
        if inclusive: #start と end も含めるなら
            return (point - start) * (start - end) * (end - point) >= 0
        return (point - start) * (start - end) * (end - point) > 0
    
    def mid_point(self, a: int, b: int) -> float:
        """a,bの中点(2つ)を返す。(n,a,b)=(3,1,2) -> 1.5, 0"""
        p1 = ((a + b) / 2) % self.n
        p2 = ((a + b + self.n) / 2) % self.n
        return p1, p2
    
    def _mod(self, *val):
        return map(lambda x: int(x) % self.n, val)
