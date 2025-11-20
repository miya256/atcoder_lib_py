class Diameter(Graph):
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
    
    def find_farthest(self) -> list[tuple[int, int]]:
        """すべてのvについて、vから最も遠い点までの(距離,頂点)を求める"""
        diameter, end1, end2 = self.diameter()
        dist1 = [diameter] * self.n
        dist2 = [diameter] * self.n
        self._dfs(end1, dist1)
        self._dfs(end2, dist2)
        #end1, end2まで同じ距離の場合は、番号が大きいほうが採用される
        return [max((d1, end1), (d2, end2)) for d1, d2 in zip(dist1, dist2)]