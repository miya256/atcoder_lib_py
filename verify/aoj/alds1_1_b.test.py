# competitive-verifier: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/1/ALDS1/1/ALDS1_1_B

from library.math.factor.gcd_lcm import gcd

x, y = map(int,input().split())
print(gcd(x, y)+1)