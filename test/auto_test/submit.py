from functools import cmp_to_key

def compare(s1, s2):
    if s1+s2 > s2+s1:
        return 1
    elif s1+s2 < s2+s1:
        return -1
    return 0

def solve():
    n = int(input())
    s = [list(input()) for _ in range(n)]
    s.sort(key=cmp_to_key(compare))
    for i in range(n-1):
        if s[i] == s[i+1]:
            for i in range(n):
                s[i] = ''.join(s[i])
            return ''.join(s)
    s[-2], s[-1] = s[-1], s[-2]
    for i in range(n):
        s[i] = ''.join(s[i])
    return ''.join(s)

ans = []
for _ in range(int(input())):
    ans.append(solve())

print(*ans)