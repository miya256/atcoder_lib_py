# competitive-verifier: PROBLEM https://judge.yosupo.jp/problem/two_sat

from library.graph.directed.twosat import TwoSAT

p, cnf, n, m = input().split()
g = TwoSAT(int(n))
for _ in range(int(m)):
    a, b, _ = map(int, input().split())
    g.add_clause(abs(a) - 1, a > 0, abs(b) - 1, b > 0)

if g.satisfiable():
    print("s", "SATISFIABLE")
    ans = [i if bi else -i for i, bi in enumerate(g.answer(), 1)]
    print("v", *ans, 0)
else:
    print("s", "UNSATISFIABLE")
