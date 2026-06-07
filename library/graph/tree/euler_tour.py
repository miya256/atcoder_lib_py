from library.graph.tree.tree import Tree


def euler_tour(t: Tree, root: int):
    """
    1step: 頂点を出る -> 辺を通る -> 頂点に入る

    parent[v]            : 頂点vの親
    in_time[v]           : 頂点vに入ったstep
    out_time[v]          : 頂点vを出たstep
    visit[i]             : step i に入った頂点
    node_weight[i]       : step i に初めて(入った,出た)頂点の重み(w,0)
    signed_node_weight[i]: step i に初めて(入った,出た)頂点の重み(w,-w)
    edge_weight[i]       : step i に(葉,根)の方向に通った辺の重み(w,0)
    signed_edge_weight[i]: step i に(葉,根)の方向に通った辺の重み(w,-w)
    depth[i]             : step i に入った頂点の深さ


    頂点vの深さ      : depth[in_time[v]]
    頂点vの重み      : node_weight[in_time[v]]
                    : signed_node_weight[out_time[v]]
    辺(par, ch)の重み: edge_weight[in_time[ch]]
                    : signed_edge_weight[out_time[ch]]

    vを根とする部分木の頂点の重み和:
        l = in_time[v]
        r = out_time[v]
        sum(node_weight[l: r])
    vを根とする部分木の辺の重み和:
        l = in_time[v] + 1
        r = out_time[v]
        sum(node_weight[l: r])
    u, vのlca:
        l = min(in_time[u], in_time[v])
        r = max(out_time[u], out_time[v])
        step = min(depth[l: r]) の index
        visit[step]
    根からvまでの頂点の重み和:
        l = 0
        r = in_time[v] + 1
        sum(signed_node_weight[l: r])
    根からvまでの辺の重み和:
        l = 0
        r = in_time[v] + 1
        sum(signed_edge_weight[l: r])
    uv間の頂点の重み和:
        根からの重みを、uw, vw, lcaw とおくと
        uw + vw - 2*lcaw + 頂点lcaの重み
    uv間の辺の重み和:
        根からの重みを、uw, vw, lcaw とおくと
        uw + vw - 2*lcaw
    """
    parent = [-1] * t.n
    in_time = [-1] * t.n
    out_time = [-1] * t.n
    visit = []
    node_weight = []
    signed_node_weight = []
    edge_weight = []
    signed_edge_weight = []
    depth = []

    stack = [(root, 1, 0, 0)]
    # (入った頂点、入った/出た 頂点の重み、通った辺の重み、入った頂点の深さ)
    while stack:
        u, vw, ew, d = stack.pop()

        if u >= 0:
            in_time[u] = len(visit)
            visit.append(u)
            node_weight.append(vw)
            signed_node_weight.append(vw)
            edge_weight.append(ew)
            signed_edge_weight.append(ew)
            depth.append(d)
            out_time[u] = len(visit)

            for v, w in t(u):
                if v != parent[u]:
                    parent[v] = u
                    stack.append((~u, -1, -w, d))
                    stack.append((v, 1, w, d + 1))
        else:
            visit.append(~u)
            node_weight.append(0)
            signed_node_weight.append(vw)
            edge_weight.append(0)
            signed_edge_weight.append(ew)
            depth.append(d)
            out_time[~u] = len(visit)

    node_weight.append(0)
    signed_node_weight.append(-1)

    return (
        parent,
        in_time,
        out_time,
        visit,
        node_weight,
        signed_node_weight,
        edge_weight,
        signed_edge_weight,
        depth,
    )
