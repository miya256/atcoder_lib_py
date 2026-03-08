class EulerTour:
    def __init__(self, n, vxWgt=None):
        """
        n: 頂点数, vxWgt: 頂点の重みリスト

        1step: 頂点を出る -> 辺を通る -> 頂点に入る\n
        頂点vに関する情報は、inTime[v]をindexとしてアクセス\n
        範囲の話\n
        頂点vの部分木の頂点について: [inTime[v], outTime[v])\n
        頂点vの部分木の辺について　: (inTime[v], outTime[v])\n

        inTime[i]  : 頂点iに入ったstep
        outTime[i] : 頂点iを出たstep
        visit[i]   : step[i]に入った頂点
        vxWgt1[i]  : step[i]に初めて(入った,出た)頂点の重み(w,0)
        vxWgt2[i]  : step[i]に初めて(入った,出た)頂点の重み(w,-w)
        edgeWgt1[i]: step[i]に(葉,根)の方向に通った辺の重み(w,0)
        edgeWgt2[i]: step[i]に(葉,根)の方向に通った辺の重み(w,-w)
        depth[i]   : step[i]に入った頂点の深さ
        depth2[i]  : 行きがけで入った深さ。帰りの場合は-1
        
        edges[i]   : 辺iの端点,重み(u,v,w)
        vertices[i] : 頂点iの重み
        """
        self.n = n
        self.tree = [[] for _ in range(n)]
        self.edges = [] #辺iの端点,重み(u,v,w)
        self.vertices = vxWgt if vxWgt else [1]*n #頂点iの重み

        self.inTime = [0]*n  #頂点iに入ったstep
        self.outTime = [0]*n #頂点iを出たstep
        self.visit = []      #step[i]に入った頂点
        self.vxWgt1 = []     #step[i]に初めて(入った, 出た)頂点の重み(w,0)
        self.vxWgt2 = []     #step[i]に初めて(入った, 出た)頂点の重み(w,-w)
        self.edgeWgt1 = []   #step[i]に(親->子, 子->親)の方向に通った辺の重み(w,0)
        self.edgeWgt2 = []   #step[i]に(親->子, 子->親)の方向に通った辺の重み(w,-w)
        self.depth = []      #step[i]に入った頂点の深さ
        self.depth2 = []     #step[i]に初めて入った頂点の深さ(帰りの場合は-1)
        self.called = False
    
    def build(self, root=0):
        """rootを根として実行する"""
        self._dfs(root)
        self.called = True
    
    def add_edge(self, u, v, w=1):
        self.tree[u].append((v, w))
        self.tree[v].append((u, w))
        self.edges.append((u, v, w))
    
    def get_edge(self, i):
        """辺iの（端点(親), 端点(子), 重み）を返す"""
        u, v, w = self.edges[i]
        if self.depth[self.inTime[u]] > self.depth[self.inTime[v]]:
            u, v = v, u
        return (u, v, w)
    
    def _dfs(self, root):
        visited = [False]*self.n
        stack = [(root, self.vertices[root], 0, 0)]
        #(入った頂点、追加すべき頂点の重み、追加すべき辺の重み、入った頂点の深さ)
        while stack:
            v,vw,ew,d = stack.pop()

            self.visit.append(v)
            self.vxWgt1.append(0 if visited[v] else vw)
            self.vxWgt2.append(vw)
            self.edgeWgt1.append(0 if visited[v] else ew)
            self.edgeWgt2.append(ew)
            self.depth.append(d)
            self.depth2.append(-1 if visited[v] else d)
            self.outTime[v] = len(self.visit)

            if not visited[v]:
                self.inTime[v] = len(self.visit)-1
                visited[v] = True
                for nv, w in self.tree[v]:
                    if not visited[nv]:
                        stack.append(( v, -self.vertices[nv], -w,   d))
                        stack.append((nv,  self.vertices[nv],  w, d+1))
        
        self.vxWgt2.append(-self.vertices[root])

#SegmentTree必要
class SubTree(EulerTour):
    def __init__(self, n):
        super().__init__(n)
        self.segVxWgt1 = None
        self.segEdgeWgt1 = None
    
    def build(self, root, op, e):
        super().build(root)
        self.segVxWgt1 = SegmentTree(op, e, self.vxWgt1)
        self.segEdgeWgt1 = SegmentTree(op, e, self.edgeWgt1)
    
    def get_vertex_weight(self, v):
        """頂点vの重みを取得"""
        return self.segVxWgt1[self.inTime[v]]
    
    def get_edge_weight(self, u, v):
        """u,vを結ぶ辺の重みを取得"""
        v = [u,v][self.depth[self.inTime[u]] < self.depth[self.inTime[v]]]
        return self.segEdgeWgt1[self.inTime[v]]
    
    def set_vertex_weight(self, v, w):
        """頂点vの重みをwに"""
        assert self.called, "build(root)関数を実行してください"
        self.segVxWgt1.set(self.inTime[v], w)
    
    def set_edge_weight(self, u, v, w):
        """u,vを結ぶ辺の重みをwに"""
        assert self.called, "build(root)関数を実行してください"
        v = [u,v][self.depth[self.inTime[u]] < self.depth[self.inTime[v]]]
        self.segEdgeWgt1.set(self.inTime[v], w)
    
    def prod_vertex_weight(self, v):
        """vを根とする部分木の頂点について、重みをprod"""
        assert self.called, "build(root)関数を実行してください"
        l = self.inTime[v]
        r = self.outTime[v]
        return self.segVxWgt1.prod(l, r)
    
    def prod_edge_weight(self,v):
        """vを根とする部分木の辺について、重みをprod"""
        assert self.called, "build(root)関数を実行してください"
        l = self.inTime[v]
        r = self.outTime[v]
        return self.segEdgeWgt1.prod(l+1, r)
    

class Path(EulerTour):
    INF = 1<<61

    def __init__(self, n):
        super().__init__(n)
        self.segDepth = None
        self.segVxWgt2 = None
        self.segEdgeWgt2 = None
    
    def build(self, root):
        super().build(root)
        self.segDepth = SegmentTree(min, self.INF, self.depth)
        self.segVxWgt2 = SegmentTree(lambda x,y:x+y, 0, self.vxWgt2)
        self.segEdgeWgt2 = SegmentTree(lambda x,y:x+y, 0, self.edgeWgt2)
    
    def lca(self, u, v):
        assert self.called, "build(root)関数を実行してください"
        l = min(self.inTime[u], self.inTime[v])
        r = max(self.outTime[u], self.outTime[v])
        min_depth = self.segDepth.prod(l, r)
        step = self.segDepth.max_right(l, lambda x:x > min_depth)
        return self.visit[step]
    
    def set_vertex(self, v, w):
        """頂点vの重みをwに"""
        assert self.called, "build(root)関数を実行してください"
        self.segVxWgt2.set(self.inTime[v], w)
        self.segVxWgt2.set(self.outTime[v], -w)
    
    def set_edge(self, u, v, w):
        """u,vを結ぶ辺の重みをwに"""
        assert self.called, "build(root)関数を実行してください"
        v = [u,v][self.depth[self.inTime[u]] < self.depth[self.inTime[v]]]
        self.segEdgeWgt2.set(self.inTime[v], w)
        self.segEdgeWgt2.set(self.outTime[v], -w)
    
    def rootVertexPath(self, v):
        """根からvまでのpathの頂点のコストの和"""
        assert self.called, "build(root)関数を実行してください"
        return self.segVxWgt2.prod(0, self.inTime[v]+1)
    
    def rootEdgePath(self, v):
        """根からvまでのpathの辺のコストの和"""
        assert self.called, "build(root)関数を実行してください"
        return self.segEdgeWgt2.prod(1, self.inTime[v]+1)
    
    def vertexPath(self, u, v):
        """uからvのpathの頂点のコストの和"""
        assert self.called, "build(root)関数を実行してください"
        uw = self.rootVertexPath(u)
        vw = self.rootVertexPath(v)
        lca = self.lca(u,v)
        lcaw = self.rootVertexPath(lca)
        return uw + vw - 2*lcaw + self.vxWgt2[self.inTime[lca]]
    
    def edgePath(self, u, v):
        """uからvのpathの辺のコストの和"""
        assert self.called, "build(root)関数を実行してください"
        uw = self.rootEdgePath(u)
        vw = self.rootEdgePath(v)
        lcaw = self.rootEdgePath(self.lca(u,v))
        return uw + vw - 2*lcaw