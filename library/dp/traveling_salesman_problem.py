from typing import Callable

inf = 1 << 61


def tsp(n: int, start: int, end: int, dist: Callable[[int, int], int]) -> int:
    """
    巡回セールスマン問題
    start からすべての点を経由して end までいく最短距離
    start = end の場合は１周
    dist(i,j): iとjの距離を返す関数
    """
    # すでに訪れた集合がs、最後に訪れたのがi、の最小値
    dp = [[inf] * n for _ in range(1 << n)]
    dp[1 << start][start] = 0

    for s in range(1 << n):
        for i in range(n):  # i -> j へ移動
            if not s >> i & 1:
                continue
            for j in range(n):
                if s >> j & 1:
                    continue
                dp[s | 1 << j][j] = min(dp[s | 1 << j][j], dp[s][i] + dist(i, j))

    if start != end:
        return dp[-1][end]
    return min(dp[-1][i] + dist(i, end) for i in range(n))
