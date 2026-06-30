# competitive-verifier: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/1/ALDS1/10/ALDS1_10_C

from library.dp.longest_common_subsequence import lcs

for _ in range(int(input())):
    s = input()
    t = input()
    print(lcs(s, t))
