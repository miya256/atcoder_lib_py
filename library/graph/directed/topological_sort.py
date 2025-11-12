from heapq import heapify, heappush, heappop

class TopologicalSorter(Graph):
    """
        トポロジカルソート\n
        サイクルがあるならNone\n
        辞書順とかにしたい場合はkeyを指定

        Attributes:
            is_dag   : グラフがDAGか（サイクルが含まれてないか）
            is_unique: トポロジカル順が一意に定まるか
        
        Methods:
            sort(key=None): keyを指定した場合はkahn
            _dfs          : O(n+m)
            _kahn         : O((n+m)log(n+m))
            has_cycle     : サイクルがあるか
            is_dag        : グラフがDAGか
            is_unique     : トポロジカル順が一意に定まるか
        """

    def __init__(self, n: int) -> None:
        super().__init__(n)
        self._is_dag: bool | None = None
        self._is_unique: bool | None = None
    
    def sort(self, key=None) -> list[int] | None:
        """トポロジカルソート"""
        self._is_dag = None
        self._is_unique = None
        if key is None:
            return self._sort_by_dfs()
        return self._sort_by_kahn(key)
    
    def has_cycle(self) -> bool:
        return not self.is_dag
    
    def _sort_by_dfs(self) -> list[int] | None:
        """帰りがけ順にやるだけ。サイクルがあるならNone"""
        UNVISITED = -1
        VISITING = 0
        VISITED = 1
        def dfs(u: int) -> bool:
            stack = [u]
            while stack:
                u = stack.pop()
                if u >= 0:
                    if visit_state[u] == VISITING:
                        return False
                    if visit_state[u] == VISITED:
                        continue
                    visit_state[u] = VISITING
                    stack.append(~u) #帰り用
                    for v in self[u]:
                        if visit_state[v] != VISITED:
                            stack.append(v)
                else:
                    u = ~u
                    visit_state[u] = VISITED
                    if postorder and postorder[-1] not in self[u]:
                        self._is_unique = False
                    postorder.append(u)
            return True

        postorder = []
        visit_state = [UNVISITED for _ in range(self._n)]
        for v in range(self._n):
            if visit_state[v] == UNVISITED:
                if not dfs(v): #DAGではないなら
                    self._is_dag = False
                    return None
        
        if self._is_unique is None: #falseにならなかったなら一意に定まる
            self._is_unique = True
        self._is_dag = True
        return postorder[::-1]
    
    def _sort_by_kahn(self, key=lambda x: x) -> list[int] | None:
        """
        入次数が0のやつから順に
        辞書順とかにしやすい
        """
        def calc_in_degree():
            in_degree = [0] * self._n
            for _, v, _ in self.edges:
                in_degree[v] += 1
            return in_degree

        in_degree = calc_in_degree()
        hq = [(key(v), v) for v, deg in enumerate(in_degree) if deg == 0]
        heapify(hq)

        order = []
        while hq:
            if len(hq) > 1:
                self._is_unique = False
            _, u = heappop(hq)
            order.append(u)
            for v in self[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    heappush(hq, (key(v), v))
        
        if self._is_unique is None:
            self._is_unique = True
        if len(order) != self._n:
            self._is_dag = False
            return None
        self._is_dag = True
        return order
    
    @property
    def is_dag(self) -> bool:
        """有向非巡回グラフ（DAG）か"""
        if self._is_dag is not None:
            return self._is_dag
        self.sort()
        return self._is_dag
    
    @property
    def is_unique(self) -> bool:
        """トポロジカルソートが一意に定まるか"""
        if self._is_unique is not None:
            return self._is_unique
        self.sort()
        return self._is_unique