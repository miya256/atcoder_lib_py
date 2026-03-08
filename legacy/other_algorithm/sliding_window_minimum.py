#スタックのやつとかもこれの応用
from collections import deque

def sliding_window_minimum(a,k):
    #min_index[i]: [max(0,i-k+1):i]の最小値のindex
    min_index = [0] * len(a)
    dq = deque()
    for i in range(len(a)):
        while dq and dq[0] <= i-k:
            dq.popleft()
        while dq and a[dq[-1]] > a[i]:
            dq.pop()
        dq.append(i)
        min_index[i] = dq[0]
    return min_index

def sliding_window_maximum(a,k):
    #max_index[i]: [max(0,i-k+1):i]の最大値のindex
    max_index = [0] * len(a)
    dq = deque()
    for i in range(len(a)):
        while dq and dq[0] <= i-k:
            dq.popleft()
        while dq and a[dq[-1]] < a[i]:
            dq.pop()
        dq.append(i)
        max_index[i] = dq[0]
    return max_index