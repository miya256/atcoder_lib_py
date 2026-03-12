# ruff: noqa

from collections import deque

n, W = map(int, input().split())
dp = [0] * (W + 1)
for i in range(n):
    v, w, c = map(int, input().split())
    ndp = [0] * (W + 1)
    for r in range(w):  # wで割った余りがrの遷移をやる
        dq = deque()
        adjusted = lambda j: dp[j] - j // w * v  # max(dp[kw+r]-kv)を求めたいから
        # スライド最大値
        for j in range(r, W + 1, w):  # ndp[j]を求める
            # 最大c個までだからそれより前の値はもういらない
            while dq and dq[0] < j - c * w:
                dq.popleft()
            while dq and adjusted(dq[-1]) < adjusted(j):
                dq.pop()
            dq.append(j)
            ndp[j] = adjusted(dq[0]) + j // w * v  # max(dp[kw+r]-kv) + tv
    dp = ndp
print(max(dp))
