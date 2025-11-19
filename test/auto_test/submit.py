n,k = map(int,input().split())
s = input()
t = []
for i in range(n-k+1):
    t.append(s[i:i+k])
from collections import deque,defaultdict,Counter

c = Counter(t)
x = max(c.values())

ans = []
for k,v in c.items():
    if v == x:
        ans.append(k)
ans.sort()
print(x)
print(*ans)