def parallel_binary_search(oks: list[int], ngs: list[int], *args) -> list[int]:
    """
    並列二分探索
    判定するのに、前から順に計算しないといけない場合
    """
    task_count = len(oks)
    for i in range(task_count):
        ngs[i] += 1 if oks[i] < ngs[i] else -1
    
    steps = max(max(oks), max(ngs))
    tasks = [[] for _ in range(steps)]
    while any(abs(ok - ng) > 1 for ok, ng in zip(oks, ngs)):
        for i in range(task_count):
            mid = (oks[i] + ngs[i]) // 2
            tasks[mid].append(i) # mid番目まで進めたら判定するから
        
        for i in range(steps): # 1stepずつ進めていき
            while tasks[i]: # i = mid になったら対応するやつを判定する
                task = tasks[i].pop()
                if satisfies(task, i):
                    oks[task] = i
                else:
                    ngs[task] = i
            # 1ステップ進める
    return oks
        
        