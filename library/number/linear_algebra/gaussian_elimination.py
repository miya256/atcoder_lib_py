def gaussian_eliminate(a: Matrix) -> int:
    """掃き出し法"""
    rank = 0
    for j in range(a.m):
        if a[rank, j] == 0:
            for i in range(rank+1, a.n):
                if a[i, j]:
                    a.swap_rows(rank, i)
                    break
            else:
                continue
        a.multiply_row(rank, pow(a[rank, j], a.Mod-2, a.Mod))
        for i in range(a.n):
            if i != rank and a[i, j]:
                a.add_row_multiple(i, rank, -a[i, j])
        rank += 1
    return rank


def solve_linear_eq(a: Matrix, b: Matrix) -> list[list[int]] | None:
    """連立方程式の解"""
    c = a.join_columns(b)
    rank = gaussian_eliminate(c)

    # rank以降の行はすべて0になるはずなので、そうでなかったら解なし
    if any(c[i, a.m] for i in range(rank, a.n)):
        return None
    
    res = [[0] * a.m for _ in range(a.m - rank + 1)]
    const = []
    var = []

    # 定数項、未定定数とそうでないものを決める
    i = 0
    for j in range(a.m):
        if c[i, j] == 1:
            res[0][j] = c[i, a.m]
            var.append(j)
            i += 1
        else:
            const.append(j)
    
    for i, j in enumerate(const, 1): # 未定定数xjが係数のベクトルを求める
        res[i][j] = 1
        for k, v in enumerate(var):
            if v > j: # j以降はすべて0だから
                break
            res[i][v] = -c[k, j] % a.Mod
    # x = a0 + c1a1 + c2a2 + ...（cは未定定数）として 
    # res[i] = ai
    return res