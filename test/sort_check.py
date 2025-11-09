def insertion_sort(a, b):
    for i in range(len(a)):
        p = i
        while p > 0:
            if a[p-1] > a[p]:
                a[p-1], a[p] = a[p], a[p-1]
            p -= 1
            if a == b:
                return True
    return False

def selection_sort(a, b):
    for i in range(len(a)):
        idx = a.index(min(a[i:]))
        a[i], a[idx] = a[idx], a[i]
        if a == b:
            return True
    return False

def bubble_sort(a, b):
    for _ in range(len(a)):
        for i in range(len(a)-2, -1, -1):
            if a[i] > a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
            if a == b:
                return True
    return False

def merge_sort(a, b):
    rng = []
    def dfs(l,r):
        if l+1 == r:
            return
        m = (l+r)//2
        dfs(l,m)
        dfs(m,r)
        rng.append((l,r))
    
    dfs(0, len(a))
    for l,r in rng:
        a[l:r] = sorted(a[l:r])
        if a == b:
            return True
    return False

def quick_sort(a, b):
    for p in [3]:
        l,r = 0,len(a)-1
        ca = list(a)
        while l < r:
            while l < r and ca[l] < p:
                l += 1
            while l < r and ca[r] >= p:
                r -= 1
            ca[l], ca[r] = ca[r], ca[l]
            l += 1
            r -= 1
            if ca == b:
                return True
    return False

from heapq import heapify,heappush,heappop
def heap_sort(a, b):
    hq = list(a)
    hq = list(map(lambda x:-x, hq))
    heapify(hq)
    end = []
    while hq:
        end.append(-heappop(hq))
        a = list(map(lambda x:-x, hq)) + end[::-1]
        if a == b:
            return True
    return False

def shell_sort(a, b):
    def _shell_sort(a, b, h):
        while h > 0:
            for r in range(h):
                for i in range(r,len(a),h):
                    p = i
                    while p-h >= 0:
                        if a[p-h] > a[p]:
                            a[p-h],a[p] = a[p],a[p-h]
                        p -= h
                        if a == b:
                            return True
            h >>= 1
        return False
    
    for h in 4,2,1:
        if _shell_sort(list(a),list(b),h):
            return True
    return False

def radix_sort(a, b):
    k = len(str(max(a)))
    for i in range(k):
        a.sort(key=lambda x:int(str(x)[-i-1]))
        if a == b:
            return True
    return False

def binary_search(l,r,f):
    if f(l) > f(r):
        l,r = r,l
    print("\nbinary search")
    i = 0
    while i < 5:
        m = (l+r)/2
        if f(m) < 0:
            l = m
        else:
            r = m
        i += 1
        print(f'{i}: f({m}) = {f(m)}')

def regula_falsi(l,r,f):
    if f(l) > f(r):
        l,r = r,l
    print("\nregula falsi")
    i = 0
    while i < 5:
        m = (l*f(r) - r*f(l)) / (f(r) - f(l))
        if f(m) < 0:
            l = m
        else:
            r = m
        i += 1
        print(f'{i}: f({m}) = {f(m)}')

def newton(f, f1, x0):
    """f1はfの微分"""
    print("\nnewton")
    i = 0
    while i < 5:
        x = x0 - f(x0) / f1(x0)
        x0 = x
        i += 1
        print(f'{i}: {x}')

def gcd(n, m):
    if m == 0:
        return n
    print(n%m)
    return gcd(m, n%m)
            
#sort
#a: 元の配列
#b: 途中結果
a = [4,8,7,2,1,5,6,9]
b = [2,4,7,8,1,5,6,9]

def f(x):
    return x*x-3
def f1(x): #fの微分
    return 2*x
l, r = 1, 2 #二分法やはさみうちの x座標の初期値 l < r
x0 = 1 #newton法の初期値

n, m = 115522, 109153


print("v"*64)
if insertion_sort(list(a), list(b)): print("insertion sort")
if selection_sort(list(a), list(b)): print("selection sort")
if bubble_sort(list(a), list(b)): print("bubble sort")
if merge_sort(list(a), list(b)): print("merge sort")
if quick_sort(list(a), list(b)): print("quick sort")
if heap_sort(list(a), list(b)): print("heap sort")
if shell_sort(list(a), list(b)): print("shell sort")
if radix_sort(list(a), list(b)): print("radix sort")

binary_search(l, r, f)
regula_falsi(l, r, f)
newton(f, f1, x0)

print("\ngcd")
print(gcd(n,m))