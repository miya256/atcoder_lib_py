#前までは、自作のクエリに答えるやつがまちがっていたから、
#ビジュアライザで良くなっているように見えても実際には悪化していた
#これが正しいコードです。

#Moのsort順。hilbert

import random
inf = 1<<61
import time
START_TIME = time.perf_counter()
def elapsed(t): #t秒経過したか
    return time.perf_counter() - START_TIME > t

from copy import deepcopy
from sortedcontainers import SortedList,SortedSet,SortedDict
from collections import deque, defaultdict, Counter

"""
n個の都市をm個のグループにわけ、各グループの都市は連結になるようにしよう
建設する道路のコストの総和を最小化しよう

q回占える。
1回の占いでは、? l C0 C1 ... C(l-1)で、
集合Cの最小全域木の辺uv(u < v)が(u,v)の昇順に返される(l-1)本

最後の出力は、まず!を出力
その次に、グループ0の都市と辺、グループ1の都市と辺...を出力
flushしなさい
"""

"""
n: 都市数
m: グループ数
q: 占える回数
l: 1回のクエリで含められる都市数の最大値
w: 都市が存在する範囲の矩形の最大幅
g: グループiの都市数
lx,rx,ly,ry
"""

#---------クエリ用--------------------------------------------
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

class UnionFind:
    class Element:
        def __init__(self, id):
            self.id = id
            self.parent = None
            self.size = 1
        
        def merge(self, other):
            """selfにotherをmerge"""
            other.parent = self
            self.size += other.size
        
        def compare(self, other):
            """selfにotherをmergeするとき、こうなっていればokというのを返す"""
            return self.size > other.size
        
        def __str__(self):
            return f'{self.id}'
            
    def __init__(self, n=0):
        self._n = n #頂点数
        self._component_count = n #連結成分の個数
        self._elements = {i: self.Element(i) for i in range(n)}
    
    def element(self, id) -> Element:
        """頂点idをElement型で取得"""
        return self._elements[id]
    
    def __getitem__(self, id):
        return self.element(id)
    
    def add(self, id):
        """頂点を追加する"""
        self._add(id)
    
    def exist(self, id):
        """点idが存在するか"""
        return self._exist(id)
    
    def __contains__(self, id):
        """in演算子で呼べる"""
        return self.exist(id)
    
    def leader(self, v):
        """頂点vの属する連結成分の根"""
        return self._leader(self._elements[v]).id
    
    def merge(self, u, v):
        """u, vを連結"""
        return self._merge(self._elements[u], self._elements[v])
    
    def same(self, u, v):
        """u,vが連結か"""
        return self._same(self._elements[u], self._elements[v])
    
    def size(self, v):
        """vの属する連結成分の要素数"""
        return self._size(self._elements[v])
    
    def roots(self):
        """根を列挙"""
        return self._roots()
    
    def members(self, v):
        """vの属する連結成分の要素"""
        return self._members(self._elements[v])
    
    def groups(self):
        """根と連結成分の要素を全列挙"""
        return self._groups()
    
    def count_components(self):
        """連結成分の個数"""
        return self._component_count
    
    def __str__(self):
        return f'{self.groups()}'
    

    def _add(self, id):
        if id in self._elements:
            return
        self._elements[id] = self.Element(id)
        self._n += 1
        self._component_count += 1
    
    def _exist(self, id):
        return id in self._elements
    
    def _leader(self, v: Element) -> Element:
        if v.parent:
            stack = []
            while v.parent:
                stack.append(v)
                v = v.parent
            while stack:
                stack.pop().parent = v
        return v
    
    def _merge(self, u: Element, v: Element):
        ru = self._leader(u)
        rv = self._leader(v)
        if ru == rv:
            return False
        self._component_count -= 1
        if not ru.compare(rv):
            ru, rv = rv, ru
        ru.merge(rv) #ruにrvをmerge
        return True
    
    def _same(self, u: Element, v: Element):
        return self._leader(u) == self._leader(v)
    
    def _size(self, v: Element):
        return self._leader(v).size
    
    def _roots(self):
        return [i for i, v in self._elements.items() if v.parent is None]
    
    def _members(self, v: Element):
        rv = self._leader(v)
        return [i for i, v in self._elements.items() if self._leader(v) == rv]
    
    def _groups(self):
        group = {}
        for i, v in self._elements.items():
            group.setdefault(self._leader(v).id, []).append(i)
        return group


def make_query_ans(cities):
    def dist(i,j):
        xi,yi = xy_for_local[i]
        xj,yj = xy_for_local[j]
        return int(((xi-xj)*(xi-xj) + (yi-yj)*(yi-yj)) ** 0.5)
    
    query_ans = []
    edges = []
    for i in range(len(cities)-1):
        for j in range(i+1, len(cities)):
            edges.append((cities[i].id, cities[j].id, dist(cities[i].id,cities[j].id)))
    uf = UnionFind()
    edges.sort(key=lambda x:x[-1])
    for u,v,_ in edges:
        uf.add(u)
        uf.add(v)
        if uf.same(u,v):
            continue
        query_ans.append((min(u,v),max(u,v)))
        uf.merge(u,v)
    return query_ans

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#---------クエリ用--------------------------------------------
    
class City:
    def __init__(self, id, lx, rx, ly, ry):
        self.id = id
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
    
    def center(self):
        return (
            (self.lx + self.rx) // 2,
            (self.ly + self.ry) // 2
        )

class Group:
    def __init__(self, n):
        self.n = n #このグループの都市数
        self.cities = []
        self.edges = []
        self.q = 0
    
    def add_city(self, city):
        self.cities.append(city)
    
    def add_edge(self, u, v):
        self.edges.append((u, v))
    
    def sat_city(self):
        """すでにn個の都市があるか"""
        return len(self.cities) == self.n
    
    def print(self):
        city_ids = [city.id for city in self.cities]
        print(*city_ids, flush=True)
        for u, v in self.edges:
            print(u, v, flush=True)


def query(cities):
    global q
    assert 2 <= len(cities) <= l

    if q <= 0:
        return [(cities[i].id, cities[i+1].id) for i in range(len(cities)-1)]
    if len(cities) == 2:
        return [(cities[0].id, cities[1].id)]

    q -= 1 
    if islocal:
        return make_query_ans(cities)
    city_ids = [city.id for city in cities]
    print("?", len(cities), *city_ids, flush=True)
    return [tuple(map(int,input().split())) for _ in range(len(cities)-1)]

def center_dist(city1, city2):
    x1,y1 = city1.center()
    x2,y2 = city2.center()
    return int(((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) ** 0.5)

def has_intersection(city1, city2):
    """2つ領域が交差しているか"""
    if city1.rx < city2.lx: return False
    if city1.lx > city2.rx: return False
    if city1.ry < city2.ly: return False
    if city1.ly > city2.ry: return False
    return True

def binary_search(ok,ng,*args):
    def satisfies(x,*args):
        """MSTを聞くとき、前の頂点をx個含められるか"""
        query_cnt = 0
        for g_size in g:
            if g_size > 2:
                query_cnt += max(0, (g_size-x-1) // (l-x)) + 1
        return query_cnt <= q

    ng += 1 if ok < ng else -1
    while abs(ok-ng) > 1:
        mid = (ok+ng)//2
        if satisfies(mid,*args):
            ok = mid
        else:
            ng = mid
    return ok

def make_group():
    def hilbert(city):
        maxn = 1 << (pow(10,5)-1).bit_length()
        x, y = city.center()
        d = 0
        s = maxn >> 1
        while s:
            rl = ((x & s) > 0)
            rr = ((y & s) > 0)
            d += s * s * ((rl * 3) ^ rr)
            if rr:
                s >>= 1
                continue
            if rl:
                x = maxn-1 - x
                y = maxn-1 - y
            x,y = y,x
            s >>= 1
        return d
    
    def calc_split_threshold():
        adj_dists = []
        for i in range(n-1):
            adj_dists.append(center_dist(sorted_cities[i], sorted_cities[i+1]))
        adj_dists.sort()
        return adj_dists[n-m]
    
    sorted_cities = sorted(cities, key=hilbert)
    split_threshold = calc_split_threshold() #区切るしきい値
    sizes = SortedList([(g[i], i) for i in range(m)], key=lambda x:x[0]) #(size, group_id)

    tmp_cities = []
    for i in range(n):
        tmp_cities.append(sorted_cities[i])
        idx = sizes.bisect_key_left(len(tmp_cities))
        if len(tmp_cities) != sizes[idx][0]:
            continue
        if len(tmp_cities) == sizes[-1][0] or center_dist(sorted_cities[i], sorted_cities[i+1]) > split_threshold:
            _, group_id = sizes.pop(idx)
            groups[group_id].cities = tmp_cities
            tmp_cities = []
        elif random.random() < 0.01:
            _, group_id = sizes.pop(idx)
            groups[group_id].cities = tmp_cities
            tmp_cities = []


def make_edge(back_cnt):
    def connect_all_min_queries(group):
        """クエリをできるだけ残す"""
        if group.n == 1:
            return
        p = 0
        while p < group.n:
            cities = []
            while len(cities) < l and p < group.n:
                cities.append(group.cities[p])
                p += 1
            if len(cities) >= 2:
                edges = query(cities)
                for u,v in edges:
                    group.add_edge(u, v)
            if p < group.n:
                group.add_edge(cities[-1].id, group.cities[p].id)
    
    def connect_all_max_queries(group):
        """グループは決定で、辺をはることに全振り"""
        def make_spanning_tree(edges):
            """まず全域木にする"""
            p = 0
            while True:
                cities = []
                while len(cities) < l and p < group.n:
                    uf.add(group.cities[p].id)
                    cities.append(group.cities[p])
                    p += 1
                edges += query(cities) * 2
                group.q -= (len(cities) > 2)

                if p == group.n:
                    break
                p -= back_cnt
        
        def add_edge_random(edges):
            cities = random.sample(group.cities, l)
            edges += query(cities)
        
        def choice_edge(edges):
            edges = Counter(edges)
            edges = [(cnt, u,v) for (u,v),cnt in edges.items()]
            edges.sort(reverse=True)
            for _,u,v in edges:
                if not uf.same(u,v):
                    group.add_edge(u,v)
                uf.merge(u,v)

        if group.n == 1:
            return
        uf = UnionFind()
        edges = []
        make_spanning_tree(edges)
        for _ in range(group.q):
            add_edge_random(edges)
        choice_edge(edges)
    

    for group in groups:
        connect_all_max_queries(group)


def distribute_queries(back_cnt):
    """各グループにクエリを振り分ける"""
    remaining_queries = q
    dq = deque(groups)
    while remaining_queries > 0 and dq:
        g = dq.popleft()
        if g.n <= 2:
            continue
        cnt = max(0, (g.n-back_cnt-1) // (l-back_cnt)) + 1
        g.q += min(cnt, remaining_queries)
        remaining_queries -= cnt
        if g.n > l:
            dq.append(g)
        

def solve():
    make_group()
    back_cnt = binary_search(1,l-1)
    distribute_queries(back_cnt)
    make_edge(back_cnt)

#入力の受け取り
islocal = True

n,m,q,l,w = map(int,input().split())
g = list(map(int,input().split()))
cities = [City(i,*map(int,input().split())) for i in range(n)]
groups = [Group(g[i]) for i in range(m)]

if islocal:
    xy_for_local = [tuple(map(int,input().split())) for _ in range(n)]

solve()

print("!", flush=True)
for group in groups:
    group.print()