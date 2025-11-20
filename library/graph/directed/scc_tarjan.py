#非再帰で書くのムズイ。なんかちがう
class SCC(Graph):
    def __init__(self, n: int, m: int) -> None:
        super().__init__(n, m)
    
    def scc(self) -> None:
        self.build()
        low = [0] * self.n
        ord = [-1] * self.n
        k = 0
        visited = [False] * self.n
        visiting = []
        ids = [0] * self.n
        groups = []

        def dfs(v: int, k: int) -> None:
            stack = [(v, v)]
            while stack:
                u, par = stack.pop()
                if u >= 0:
                    if visited[u]:
                        low[par] = min(low[par], ord[u])
                        continue
                    visited[u] = True
                    visiting.append(u)
                    ord[u] = low[u] = k
                    k += 1
                    stack.append((~u, par))
                    for v in self[u]:
                        if v != par:
                            stack.append((v, u))
                else:
                    u = ~u
                    low[par] = min(low[par], low[u])
                    if low[u] == ord[u]:
                        groups.append([])
                        while True:
                            v = visiting.pop()
                            ord[v] = self.n
                            ids[v] = len(groups)
                            groups[-1].append(v)
                            if u == v:
                                break
            return k
        
        for v in range(self.n):
            if not visited[v]:
                k = dfs(v, k)
        
        return groups[::-1], list(map(lambda x: len(groups) - x, ids))