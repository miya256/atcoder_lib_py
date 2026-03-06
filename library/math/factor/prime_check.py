def is_prime(n: int) -> bool:
    """
    ミラーラビン法
    p-1 = t * 2^s のとき
    a^(p-1)-1 = (a^(t*2^(s-1)) + 1)...(a^2t + 1)(a^t + 1)(a^t - 1)
    と因数分解できる。pが素数なら
    a^(p-1)-1 = 0 なので、因数のうちどれかは0である
    因数が0になるか1つずつ確認するだけ
    """
    if n == 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # p-1 = t * 2^s
    s, t = 0, n-1
    while t % 2 == 0:
        s += 1
        t >>= 1

    for a in (2, 7, 61, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a > n-2:
            break

        x = pow(a, t, n)

        # (a^t - 1) の確認
        # これが0 つまり a^t = 1 なら素数の可能性あり
        if x == 1:
            continue

        # (a^(t * 2^i) + 1) の確認
        # これが0 つまり a^(t * 2^i) = -1 なら素数の可能性あり
        for _ in range(s):
            if x == n-1:
                break
            x = x * x % n
        else:
            return False
        
    return True