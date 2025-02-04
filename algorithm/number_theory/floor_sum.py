def floor_sum(n, m, a, b):
    ans = 0
    while True:
        if a >= m or a < 0:
            ans += n * (n - 1) * (a // m) // 2
            a %= m
        if b >= m or b < 0:
            ans += n * (b // m)
            b %= m
        y_max = a * n + b
        if y_max < m: break
        n, b, m, a = y_max // m, y_max % m, a, m
    return ans 
