class Diameter(Graph):
    """
    木の直径

    Methods:
        diameter(): 直径と端点を返す
        dist(v)   : vからほかの点までの距離
    """
    def __init__(self, n: int) -> None:
        super().__init__(n, n-1)
    
    def _dfs(self, v: int, dist: list[int] | None = None) -> tuple[int, int]:
        """distを指定すればvからの距離、そうでなければ直径と端点"""
        stack = [(v, -1, 0)]
        end, diameter = -1, 0
        while stack:
            u, par, d = stack.pop()

            if dist is not None:
                dist[u] = d

            if diameter < d:
                diameter = d
                end = u

            for v, w in self(u):
                if v != par:
                    stack.append((v, u, d+w))
        
        return diameter, end
    
    def diameter(self) -> tuple[int, int, int]:
        """直径、端点1、端点2"""
        _, end1 = self._dfs(0)
        diameter, end2 = self._dfs(end1)
        return diameter, end1, end2
    
    def dist(self, v: int) -> list[int]:
        """vからの距離"""
        dist = [inf := 1<<61] * self.n
        self._dfs(v, dist)
        return dist
