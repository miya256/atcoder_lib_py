from atcoder.segtree import SegTree
from collections import deque

class HLD:
    def __init__(self,n,op,e):
        """
        parent : 頂点iの親
        depth  : 頂点iの深さ
        size   : 頂点iの子の数(自分を含む)
        heavy  : heavy辺に隣接するノード、heavy辺の重み
        top    : 頂点iの連結成分の根
        idx    : 頂点iのセグ木のindex
        edgeWgt : 辺の重みを並べたやつ(左ほど深い)
        """
        self.n = n
        self.op = op
        self.e = e
        self.tree = [[] for _ in range(n)]
        self.edges =[]
        self.iscall = False

        self.parent = [-1]*n
        self.depth = [0]*n
        self.size = [0]*n
        self.heavy = [(-1,-1)]*n
        self.top = [0]*n
        self.idx = [-1]*n
        self.edgeWgt = []
    
    def add_edge(self,u,v,w):
        self.tree[u].append((v,w))
        self.tree[v].append((u,w))
        self.edges.append((u,v,w))
    
    def get_edge(self,i):
        return self.edges[i]
    
    def _dfs1(self,root):
        """parent,depth,size,heavyを求める"""
        visited = [False]*self.n
        stack = deque([(root,-1,0,0)])
        while stack:
            v,prev,w,d = stack.pop()
            if visited[v]:
                if self.heavy[v][0] == -1 or self.size[self.heavy[v][0]] < self.size[prev]:
                    self.heavy[v] = (prev,w)
                self.size[v] += self.size[prev]
            else:
                self.parent[v] = prev
                self.depth[v] = d
                self.size[v] += 1

                visited[v] = True
                for nv,w in self.tree[v]:
                    if not visited[nv]:
                        stack.append((v,nv,w,d))
                        stack.append((nv,v,w,d+1))
    
    def _dfs2(self,root):
        visited = [False]*self.n
        stack = deque([(root,-1,0)])
        while stack:
            v,prev,w = stack.pop()
            self.top[v] = self.top[prev] if prev != -1 and self.heavy[prev][0] == v else v
            self.idx[v] = len(self.edgeWgt)
            self.edgeWgt.append(w)
            visited[v] = True
            for nv,w in self.tree[v]:
                if visited[nv] or nv == self.heavy[v][0]:
                    continue
                stack.append((nv,v,w))
            if self.heavy[v][0] != -1:
                nv,w = self.heavy[v]
                stack.append((nv,v,w))
    
    def build(self,root):
        self.iscall = True
        self._dfs1(root)
        self._dfs2(root)
        #左が深いほうが扱いやすいから逆にしてる
        self.idx = list(map(lambda x:len(self.idx)-x-1,self.idx))
        self.edgeWgt = self.edgeWgt[::-1]
        self.segEdgeWgt = SegTree(self.op,self.e,self.edgeWgt)
    
    def set(self,u,v,w):
        """u,vの辺の重みをwに"""
        assert self.iscall, "build(root)関数を実行してください"
        if self.parent[u] == v:
            u,v = v,u
        self.segEdgeWgt.set(self.idx[v],w)
    
    def edge_prod(self,u,v):
        """uからvまでをprod"""
        assert self.iscall, "build(root)関数を実行してください"
        res = self.e
        while True:
            ui,vi = self.idx[u],self.idx[v]
            if self.top[u] == self.top[v]:
                if self.depth[u] < self.depth[v]:
                    ui,vi = vi,ui
                res = self.op(res,self.segEdgeWgt.prod(ui,vi))
                return res
            utop,vtop = self.top[u],self.top[v]
            if self.depth[utop] < self.depth[vtop]:
                u,v = v,u
                ui,vi = vi,ui
                utop,vtop = vtop,utop
            res = self.op(res,self.segEdgeWgt.prod(ui,self.idx[utop]+1))
            u = self.parent[utop]