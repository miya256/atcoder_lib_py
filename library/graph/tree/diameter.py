from library.graph.tree.tree import Tree


def diameter(t: Tree) -> tuple[int, int, int]:
    """直径、端点1、端点2"""

    def dfs(v: int) -> tuple[int, int]:
        stack = [(v, -1, 0)]
        end, diameter = -1, -1
        while stack:
            u, par, d = stack.pop()
            if diameter < d:
                diameter = d
                end = u
            for v, w in t(u):
                if v != par:
                    stack.append((v, u, d + w))
        return diameter, end

    _, end1 = dfs(0)
    diameter, end2 = dfs(end1)
    return diameter, end1, end2
