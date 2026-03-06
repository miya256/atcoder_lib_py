class MinCostFlowGraph:
    class Edge:
        def __init__(self, dst, cap, cost):
            self.dst = dst
            self.cap = cap
            self.cost = cost
            self.rev = None
    
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.edges = []
    
    def add_edge(self, src, dst, cap, cost):
        edge = MinCostFlowGraph.Edge(dst, cap, cost)
        rev = MinCostFlowGraph.Edge(src, 0, -cost)
        edge.rev = rev
        rev.rev = edge
        self.graph[src].append(edge)
        self.graph[dst].append(rev)
        self.edges.append(edge)
    
    def edge(self, i):
        """辺iの src, dst, cap, flow, cost"""
        edge = self.edges[i]
        src = edge.rev.dst
        dst = edge.dst
        cap = edge.cap + edge.rev.cap
        flow = edge.rev.cap
        cost = edge.cost
        return src, dst, cap, flow, cost
    
    def slope(self, s, t, limit=None):
        flow = 0
        cost = 0
        result = [(flow, cost)]