from atcoder.segtree import SegTree
from collections import deque

class EulerTour:
    def __init__(self,n):
        """
        1step: 頂点を出る -> 辺を通る -> 頂点に入る

        inTime[i]: 頂点iに入ったstep
        outTime[i]: 頂点iを出たstep
        visit[i]: step[i]に入った頂点
        vxWgt1[i]: step[i]に初めて(入った,出た)頂点の重み(w,0)
        vxWgt2[i]: step[i]に初めて(入った,出た)頂点の重み(w,-w)
        edgeWgt1[i]: step[i]に(葉,根)の方向に通った辺の重み(w,0)
        edgeWgt2[i]: step[i]に(葉,根)の方向に通った辺の重み(w,-w)
        depth[i]: step[i]に入った頂点の深さ

        edges[i]: 辺iの端点,重み(u,v,w)
        vertexs[i]: 頂点iの重み
        """
        self.n = n
        self.tree = [[] for _ in range(n)]
        self.edges = []
        self.vertexs = [1]*n

        self.inTime = [0]*n
        self.outTime = [0]*n
        self.visit = []
        self.vxWgt1 = []
        self.vxWgt2 = []
        self.edgeWgt1 = []
        self.edgeWgt2 = []
        self.depth = []
        self.iscall = False
    
    def add_edge(self,u,v,w=1):
        self.tree[u].append((v,w))
        self.tree[v].append((u,w))
        self.edges.append((u,v,w))
    
    def add_vetex(self,vertexs):
        """頂点に重みを付与(重みのリストを渡す)"""
        self.vertexs = vertexs
    
    def _dfs(self,root):
        visited = [False]*self.n
        stack = deque([(root,self.vertexs[root],0,0)])
        #(入った頂点、追加すべき頂点の重み、追加すべき辺の重み、入った頂点の深さ)
        while stack:
            v,vw,ew,d = stack.pop()

            if not visited[v]: self.inTime[v] = len(self.visit)
            self.visit.append(v)
            self.vxWgt1.append(0 if visited[v] else vw)
            self.vxWgt2.append(vw)
            self.edgeWgt1.append(0 if visited[v] else ew)
            self.edgeWgt2.append(ew)
            self.depth.append(d)
            self.outTime[v] = len(self.visit)

            if not visited[v]:
                visited[v] = True
                for nv,w in self.tree[v]:
                    if not visited[nv]:
                        stack.append((v,-self.vertexs[nv],-w,d))
                        stack.append((nv,self.vertexs[nv],w,d+1))
        
        self.vxWgt2.append(-self.vertexs[root])
    
    def get_vertex(self,i):
        """頂点iの重み"""
        return self.vertexs[i]
    
    def get_edge(self,i):
        """辺iの(u,v,w)"""
        return self.edges[i]
    
    def get_depth(self,i):
        """頂点iの深さ"""
        assert self.iscall, "build(root)関数を実行してください"
        return self.depth[i]
    
    def build(self,root):
        """rootを根として実行する"""
        self.iscall = True
        self._dfs(root)


class SubTree(EulerTour):
    def __init__(self,n):
        super().__init__(n)
        self.segVxWgt1 = None
        self.segEdgeWgt1 = None
    
    def build(self,root,op,e):
        super().build(root)
        self.segVxWgt1 = SegTree(op,e,self.vxWgt1)
        self.segEdgeWgt1 = SegTree(op,e,self.edgeWgt1)
    
    def set_vertex(self,v,w):
        """頂点vの重みをwに"""
        assert self.iscall, "build(root)関数を実行してください"
        self.segVxWgt1.set(self.inTime[v],w)
    
    def set_edge(self,u,v,w):
        """u,vを結ぶ辺の重みをwに"""
        assert self.iscall, "build(root)関数を実行してください"
        v = [u,v][self.depth[self.inTime[u]] < self.depth[self.inTime[v]]]
        self.segEdgeWgt1.set(self.inTime[v],w)
    
    def prod_vertex_weight(self,v):
        """vを根とする部分木について、重みをprod"""
        assert self.iscall, "build(root)関数を実行してください"
        l = self.inTime[v]
        r = self.outTime[v]
        return self.segVxWgt1.prod(l,r)
    
    def prod_edge_weight(self,v):
        """vを根とする部分木について、重みをprod"""
        assert self.iscall, "build(root)関数を実行してください"
        l = self.inTime[v]
        r = self.outTime[v]
        return self.segEdgeWgt1.prod(l+1,r)


class LCA(EulerTour):
    def __init__(self,n):
        super().__init__(n)
        self.segDepth = None
    
    def build(self,root):
        super().build(root)
        self.segDepth = SegTree(min,float('inf'),self.depth)
    
    def lca(self,u,v):
        assert self.iscall, "build(root)関数を実行してください"
        l = min(self.inTime[u],self.inTime[v])
        r = max(self.outTime[u],self.outTime[v])
        min_depth = self.segDepth.prod(l,r)
        step = self.segDepth.max_right(l,lambda x:x > min_depth)
        return self.visit[step]
    

class Path(LCA):
    def __init__(self,n):
        super().__init__(n)
        self.segVxWgt2 = None
        self.segEdgeWgt2 = None
    
    def build(self,root):
        super().build(root)
        self.segVxWgt2 = SegTree(lambda x,y:x+y,0,self.vxWgt2)
        self.segEdgeWgt2 = SegTree(lambda x,y:x+y,0,self.edgeWgt2)
    
    def set_vertex(self,v,w):
        """頂点vの重みをwに"""
        assert self.iscall, "build(root)関数を実行してください"
        self.segVxWgt2.set(self.inTime[v],w)
        self.segVxWgt2.set(self.outTime[v],-w)
    
    def set_edge(self,u,v,w):
        """u,vを結ぶ辺の重みをwに"""
        assert self.iscall, "build(root)関数を実行してください"
        v = [u,v][self.depth[self.inTime[u]] < self.depth[self.inTime[v]]]
        self.segEdgeWgt2.set(self.inTime[v],w)
        self.segEdgeWgt2.set(self.outTime[v],-w)
    
    def rootVertexPath(self,v):
        """根からvまでのpathの頂点のコストの和"""
        assert self.iscall, "build(root)関数を実行してください"
        return self.segVxWgt2.prod(0,self.inTime[v]+1)
    
    def rootEdgePath(self,v):
        """根からvまでのpathの辺のコストの和"""
        assert self.iscall, "build(root)関数を実行してください"
        return self.segEdgeWgt2.prod(1,self.inTime[v]+1)
    
    def vertexPath(self,u,v):
        """uからvのpathの頂点のコストの和"""
        assert self.iscall, "build(root)関数を実行してください"
        uw = self.rootVertexPath(u)
        vw = self.rootVertexPath(v)
        lca = self.lca(u,v)
        lcaw = self.rootVertexPath(lca)
        return uw + vw - 2*lcaw + self.vxWgt2[self.inTime[lca]]
    
    def edgePath(self,u,v):
        """uからvのpathの辺のコストの和"""
        assert self.iscall, "build(root)関数を実行してください"
        uw = self.rootEdgePath(u)
        vw = self.rootEdgePath(v)
        lcaw = self.rootEdgePath(self.lca(u,v))
        return uw + vw - 2*lcaw