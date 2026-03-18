# verification-helper: PROBLEM https://judge.yosupo.jp/problem/longest_increasing_subsequence

from library.dp.longest_increasing_subsequence import lis

n = int(input())
a = list(map(int, input().split()))

ans = lis(a)

print(len(ans))
print(*ans)
