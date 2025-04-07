class Diameter:
    def __init__(self,n):
        self.n = n
        self.graph = [[] for _ in range(n)]
    
    def add_edge(self,u,v,w=1):
        self.graph[u].append((v,w))
        self.graph[v].append((u,w))
    
    def dfs(self,v):
        stack = [(v,-1,0)]
        end, diameter = -1,0
        while stack:
            v,par,dist = stack.pop()
            if diameter < dist:
                diameter = dist
                end = v
            for nv,w in self.graph[v]:
                if nv != par:
                    stack.append((nv,v,dist+w))
        return end, diameter
    
    def diameter(self):
        end,_ = self.dfs(0)
        return self.dfs(end)[1]