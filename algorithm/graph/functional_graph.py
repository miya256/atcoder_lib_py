from atcoder.scc import SCCGraph

class FunctionalGraph:
    #頂点iから出る辺が1つ
    def __init__(self,n):
        self.n = n
        self.graph = SCCGraph(n)
        self.g = [[] for _ in range(n)]
        self._scc = None
    
    def add_edge(self,u,v):
        self.graph.add_edge(u,v)
        self.g[u].append(v)
    
    def scc(self):
        if not self._scc:
            self._scc = self.graph.scc()
        return self._scc
    
    def make_tree(self):
        parent = [-1]*len(self.scc())
        group_num = [-1]*self.n
        for i,vertexs in enumerate(self.scc()[::-1]):
            for v in vertexs:
                group_num[v] = i
                if len(vertexs) == 1:
                    parent[i] = group_num[self.g[i][0]]
        return parent
        