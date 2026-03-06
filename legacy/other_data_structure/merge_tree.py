class MergeTree:
    def __init__(self,n):
        self.n = n
        self.parent = [i for i in range(n)]
        self.tree = [[] for _ in range(n)]

    def leader(self,v):
        if v != self.parent[v]:
            self.parent[v] = self.leader(self.parent[v])
        return self.parent[v]
    
    def merge(self,u,v):
        ru = self.leader(u)
        rv = self.leader(v)
        par = self.n
        self.n += 1
        self.parent.append(par)
        self.tree.append([])

        self.parent[ru] = par
        self.parent[rv] = par
        self.tree[ru].append(par)
        self.tree[rv].append(par)
        self.tree[par].append(ru)
        self.tree[par].append(rv)
    
    def roots(self):
        return [i for i in range(self.n) if self.parent[i] == i]