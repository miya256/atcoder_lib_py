# verification-helper: PROBLEM https://judge.yosupo.jp/problem/system_of_linear_equations

from library.math.linear_algebra.matrix import Matrix
from library.math.linear_algebra.gaussian_elimination import solve_linear_eq

n, m = map(int, input().split())
a = Matrix([list(map(int, input().split())) for _ in range(n)])
b = Matrix([list(map(int, input().split()))]).transpose()

ans = solve_linear_eq(a, b)
if ans is None:
    exit(print(-1))

print(len(ans) - 1)
for c in ans:
    print(*c)
