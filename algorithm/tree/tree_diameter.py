import sys
sys.setrecursionlimit(10**6)
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")

def dfs(v):
    stack = [(v,-1,0)]
    max_vertex, max_dist = -1,0
    while stack:
        v,par,dist = stack.pop()
        if max_dist < dist:
            max_dist = dist
            max_vertex = v
        for nv in g[v]:
            if nv != par:
                stack.append((nv,v,dist+1))
    return max_vertex, max_dist

def diameter():
    v,d = dfs(0)
    return dfs(v)[1]