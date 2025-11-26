def gaussian_eliminate(a: Matrix) -> int:
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

