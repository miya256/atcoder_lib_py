#あってるかわからん
class AuxiliaryTree:
    def __init__(self, n):
        self.n = n
        self.tree = [[] for _ in range(n)]
        self.inTime = None
        self.outTime = None
        self.visit = None
        self.depth = None
        self.sparse_table = None
        self.called = False
    
    def add_edge(self, u, v):
        self.tree[u].append(v)
        self.tree[v].append(u)

    def _prepare(self, root):
        """
        前計算。Euler Tourで
        pre-orderとLCAを高速に計算できるようにしておく
        """
        self._dfs(root)
        self.called = True
    
    def _dfs(self, root):
        """Euler Tour"""
        inTime = [0] * self.n
        outTime = [0] * self.n
        visit = []
        depth = []
        visited = [False] * self.n
        stack = [(root, 0)] #(頂点, 深さ)
        while stack:
            v, d = stack.pop()
            visit.append(v)
            depth.append(d)
            outTime[v] = len(visit)
            if not visited[v]:
                inTime[v] = len(visit)-1
                visited[v] = True
                for nv in self.tree[v]:
                    if not visited[nv]:
                        stack.append((v, d))
                        stack.append((nv, d+1))
        self.inTime = inTime
        self.outTime = outTime
        self.visit = visit
        self.depth = depth
        self.sparse_table = self._make_sparse_table(depth)
    
    def _make_sparse_table(self, depth):
        """Euler Tour + sparse tableでLCAを計算"""
        st = [[(v, i) for i, v in enumerate(depth)]]
        for i in range(1, len(depth).bit_length()):
            st.append([0] * (len(depth)-(1<<i)+1))
            for j in range(len(depth)-(1<<i)+1):
                st[i][j] = min(st[i-1][j], st[i-1][j+(1<<(i-1))])
        return st
    
    def _lca(self, u, v):
        l = min(self.inTime[u], self.inTime[v])
        r = max(self.outTime[u], self.outTime[v])
        idx = (r-l).bit_length() - 1
        _, step = min(self.sparse_table[idx][l], self.sparse_table[idx][r-(1<<idx)])
        return self.visit[step]
    
    def build(self, vertices):
        """与えられた頂点集合のAuxiliary Treeを構築"""
        if not self.called:
            self._prepare(0)
        vertices.sort(key=lambda x: self.inTime[x])
        for i in range(len(vertices)-1):
            lca = self._lca(vertices[i], vertices[i+1])
            vertices.append(lca)
        
        vertices.sort(key=lambda x: self.inTime[x])

        stk = []
        parent = {}
        pv = -1
        for v in vertices:
            if pv == v:
                continue
            while stk and self.outTime[stk[-1]] < self.inTime[v]:
                stk.pop()
            if stk:
                parent[v] = stk[-1]
            stk.append(v)
            pv = v
        parent[stk[0]] = -1
        return parent

t = AuxiliaryTree(13)
t.add_edge(0,1)
t.add_edge(0,2)
t.add_edge(2,3)
t.add_edge(3,4)
t.add_edge(4,5)
t.add_edge(4,6)
t.add_edge(4,7)
t.add_edge(7,8)
t.add_edge(2,9)
t.add_edge(9,10)
t.add_edge(10,11)
t.add_edge(9,12)
print(t.build([1,5,8,11]))