# competitive-verifier: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/1/ALDS1/9/ALDS1_9_C

from library.containers.heap.heap import Heap


def compare(p, c):
    return p > c


hq = Heap(compare)
while (query := input()) != "end":
    if query.startswith("insert"):
        n = int(query.split()[1])
        hq.push(n)
    else:
        print(hq.pop())
