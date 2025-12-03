def binary_search(ok, ng, *args):
    """二分探索"""
    def satisfies(x):
        """xのとき条件を満たすか"""
        return
    
    ng += 1 if ok < ng else -1
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if satisfies(mid):
            ok = mid
        else:
            ng = mid
    return ok