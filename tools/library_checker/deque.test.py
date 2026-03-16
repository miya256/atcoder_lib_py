# verification-helper: PROBLEM https://judge.yosupo.jp/problem/deque

from library.containers.deque import Deque

dq = Deque()
q = int(input())

for _ in range(q):
    t, *data = map(int, input().split())
    if t == 0:
        x = data[0]
        dq.appendleft(x)
    if t == 1:
        x = data[0]
        dq.append(x)
    if t == 2:
        dq.popleft()
    if t == 3:
        dq.pop()
    if t == 4:
        i = data[0]
        print(dq[i])
