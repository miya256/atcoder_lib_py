import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

def dfs(g,child,v,pre=-1):
    for nv in g[v]:
        if nv == pre:
            continue
        dfs(g,child,nv,v)
        child[v] += child[nv] + 1

def count_children(g,root):
    """木の各頂点の子孫の数(自分含まない)"""
    n = len(g)
    child = [0]*n
    dfs(g,child,root)
    return child
