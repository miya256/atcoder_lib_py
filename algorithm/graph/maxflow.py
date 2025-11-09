#非再帰にする。
#イテレータの高速化とかがあるから気を付ける。
#いままでやったことないタイプの非再帰かだぞ!

#O(N^2M)
#最大流をFとして O(FM)
#辺容量の平均がkのとき O(kM^(2/3))
#二部マッチングは O(M√N)

import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

from collections import deque
class MaxFlowGraph:
    class Edge:
        def __init__(self, dst, cap):
            self.dst = dst
            self.cap = cap #逆辺のcap=flow
            self.rev = None #逆辺のポインタ

    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = []
    
    def add_edge(self, src, dst, cap):
        """src -> dst へ容量cap の辺をはる"""
        edge = MaxFlowGraph.Edge(dst, cap)
        rev = MaxFlowGraph.Edge(src, 0)
        edge.rev = rev
        rev.rev = edge
        self.graph[src].append(edge)
        self.graph[dst].append(rev)
        self.edges.append(edge)
    
    def edge(self, i):
        """辺iの src, dst, cap, flow を返す"""
        edge = self.edges[i]
        src = edge.rev.dst
        dst = edge.dst
        cap = edge.cap + edge.rev.cap
        flow = edge.rev.cap
        return src, dst, cap, flow
    
    def _bfs(self, s):
        """levelを計算"""
        levels = [-1] * self.n
        levels[s] = 0
        dq = deque([s])
        while dq:
            v = dq.popleft()
            for edge in self.graph[v]:
                if edge.cap > 0 and levels[edge.dst] == -1:
                    levels[edge.dst] = levels[v] + 1
                    dq.append(edge.dst)
        return levels
    
    def _dfs(self, s, t, f, levels, itr):
        """今のグラフで流せるだけ流す"""
        if s == t:
            return f
        for edge in itr[s]: 
            #graph[s]だと先頭からになってしまうが、
            #イテレータをつかえばまだ見てないところから再開できる
            if edge.cap and levels[s] < levels[edge.dst]:
                flow = self._dfs(edge.dst, t, min(f, edge.cap), levels, itr)
                if flow > 0:
                    edge.cap -= flow
                    edge.rev.cap += flow
                    return flow
        return 0
    
    def flow(self, s, t):
        """s -> t の最大流"""
        flow = 0
        while True:
            levels = self._bfs(s)
            if levels[t] == -1:
                return flow
            itr = list(map(iter, self.graph))
            f = 1<<61 #inf
            while f:
                f = self._dfs(s, t, f, levels, itr)
                flow += f