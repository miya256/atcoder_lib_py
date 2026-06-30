# competitive-verifier: PROBLEM https://judge.yosupo.jp/problem/set_xor_min

from library.containers.binary_trie import BinaryTrie

bt = BinaryTrie(30)
q = int(input())
for _ in range(q):
    t, x = map(int, input().split())
    if t == 0:
        if x not in bt:
            bt.add(x)
    if t == 1:
        bt.discard(x)
    if t == 2:
        if len(bt) <= 0:
            continue
        print(bt.kth_smallest(0, x) ^ x)
