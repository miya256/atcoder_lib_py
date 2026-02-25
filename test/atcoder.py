from collections import deque, defaultdict, Counter

def solve():
    n,d = map(int,input().split())
    a = list(map(int,input().split()))
    b = list(map(int,input().split()))
    dq = deque()
    for i in range(n):
        for _ in range(a[i]):
            dq.append(i)
        for _ in range(b[i]):
            dq.popleft()
        while dq and dq[0] <= i-d:
            dq.popleft()
    print(len(dq))

for _ in range(int(input())):
    solve()