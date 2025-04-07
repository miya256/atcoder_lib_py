#再帰上限解放
#標準入力高速化
#再帰高速化
#メモ化再帰

import sys
sys.setrecursionlimit(10**6)
input = sys.stdin.readline
import pypyjit
pypyjit.set_param("max_unroll_recursion=-1")
from functools import cache
@cache

#四捨五入
from decimal import Decimal, ROUND_HALF_UP
Decimal(str(n)).quantize(Decimal('0'),ROUND_HALF_UP) #小数点以下
Decimal(str(n)).quantize(Decimal('0.1'),ROUND_HALF_UP) #小数第2位で四捨五入
Decimal(str(n)).quantize(Decimal('0.01'),ROUND_HALF_UP) #小数第3位で四捨五入
Decimal(str(n)).quantize(Decimal('1E1'),ROUND_HALF_UP) #1桁目で四捨五入
Decimal(str(n)).quantize(Decimal('1E2'),ROUND_HALF_UP) #2桁目で四捨五入

#compareをkeyにしたいとき
from functools import cmp_to_key
a.sort(key=cmp_to_key(compare))

#bisectはkeyを指定できる

#sortedcontainer
from sortedcontainers import SortedList,SortedSet,SortedDict
"""
初期化するときにkeyを指定する
|演算子で融合。融合する順番は考える必要がある
add()
discard()
pop()
スライス[:]
len()
bisect_left()
bisect_right()
bisect_key_left()
bisect_key_right()
index()
irange(l,r) : l以上r以下の要素を列挙

要素がタプルで、key=lambda x:x[0]などとしたとき、
同じタプル同士で比べることになるなら、bisect_left((x,y))のようにするが、
keyだけを指定する場合は、bisect_key_left(x)というふうにkeyがついてるメソッドを使う
"""


#アルファベット
lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


#AtCoder Library
#pypyで出す

#UnionFind
from atcoder.dsu import DSU
"""
※再帰が速くなるやつ書く

DSU(n)    : n頂点で初期化
merge(u,v): u,vを結合
same(u,v) : u,vが同じ連結成分か
leader(u) : uの連結成分の根を返す
size(u)   : uの連結成分の頂点数を返す
groups()  : 全体を返す(二次元配列)
"""
#FenwicTree
from atcoder.fenwicktree import FenwickTree
"""
FenwickTree(n): n頂点で初期化
add(i,v)      : i番目にvを加算
sum(l,r)      : [l,r)の和を返す
"""
#FloorSum
from atcoder.math import floor_sum
"""クラスではなく、関数
floor_sum(n,m,a,b) :(a*i+b)//mを i=0～n-1　まで足したものを返す
"""
#MaxFlow
from atcoder.maxflow import MFGraph
"""
MFGraph(n)        : n頂点で初期化
add_edge(u,v,c)   : uからvへ最大容量cの辺をはり、その辺の番号を返す
flow(s,t)         : sからtへの最大流を求める
get_edge(m)       : 辺mの状態(始点、終点、容量、流量)を返す
edges()           : すべての辺の状態をリストにまとめて返す
change_edge(m,c,f): 辺mの最大容量をcに、流量をfにする
min_cut(u)        : 最小カットを求める。
                    返り値は長さのリストで、i番目の要素は
                    頂点uから残余グラフで到達できるならTrueが、
                    到達できないならFalseが入っている。
"""
#MinCostFlow
from atcoder.mincostflow import MCFGraph
"""
MCFGraph(n)           : n頂点で初期化
add_edge(u,v,cap,cost): uからvに最大容量cap,コストcostのへんを張る。辺の番号を返す。
flow(u,v,lim)         : uからvへ最大流量limまで流せるだけ流す。limは省略可能。
                        (最大フロー、最小コスト)のタプルを返す
slope(u,v,lim)　　　　: flowと同じだが、(流量、コスト)の折れ線グラフを返す。
get_edge(i)           : 番号iの辺の状態(始点、終点、最大流量、流量、コスト)を返す。
edges()               : すべての辺の状態をリストにまとめて返す
"""
#Convolution(TLEするらしい)
from atcoder.convolution import convolution
"""クラスではなく、関数
convolution(m,a,b): 畳み込みを計算(mod m)
"""
#SCC
from atcoder.scc import SCCGraph
"""
SCCGraph(n)  : n頂点で初期化
add_edge(u,v): uからvへ辺を張る
scc()        : 強連結成分分解(二次元リスト、トポロジカルソートされている)
"""
#2-SAT
from atcoder.twosat import TwoSAT
"""
TowSAT(n)          : n頂点で初期化
add_clause(i,f,j,g): (xi = f)V(xj = g)の条件式を追加する
satisfiable()      : 条件を満たすようにx1,x2,...,xnに真偽を割り当てられるか
answer()           :最後に呼んだsatisfiable()のときの
                    x1,x2,...,xnの真偽値のリストを返す
"""
#Number of Substrings
from atcoder.string import suffix_array, lcp_array, z_algorithm
"""クラスではなく、関数
suffix_array(s): 文字列Sのsuffix(接尾辞)-arrayとして、長さ|S|のリストを返す
                 suffix-arrayの説明はABC272-F　(1~nをS[i:]を基準にsortしたもの)
lcp_array(s,sa): 文字列SのLCP-arrayとして、長さ|S|-1のリストを返す
                 lcp-arrayとは、suffix-arrayにおいて、i番目とi+1番目のsuffixのLCPの長さを格納したもの
z_algorithm(s) : 長さ|S|のリスト。i番目はSとS[i:]の最長共通接頭辞の長さ
"""
#SegmentTree
from atcoder.segtree import SegTree
"""
SegTree(op,e,v)  : op,eは関数、単位元。vはlistかintを入れる。
set(p,x)         : p番目にxを代入
get(p)           : p番目の要素を返す
prod(l,r)        : [l,r)の演算結果
all_prod()       : [0,n)の演算(全体ということ)
max_right(p,func): prod[p,j)でfuncを満たす最大のjを返す。
min_left(p,func) : prod[j,p)でfuncを満たす最小のjを返す。
                   つまりfunc(prod(p,j))=Trueとなる最大のjってこと
                   pより右でfを満たす最小の...だったら、pより右でfを満たさない最大のとすればよい
"""
#LazySegmentTree
from atcoder.lazysegtree import LazySegTree
"""
xは要素とは限らず、２冪の範囲についての値である。ABC357Fが勉強になる

LazySegTree(op, e, mapping, composition, _id, lst)
            op(a,b)         : 区間取得の演算
            e               : opの単位元
            mapping(f,x)    : dataにlazyを作用( xはdata,fは作用素)
            composition(f,g): lazyとlazyを合成( fは後の操作,gは前の操作)
            _id             : mappingの恒等写像(単位元？)
            lis             : 初期リスト(sizeがほしいときは、lst = [(a, 1) for a in A]
apply(l,r,f)     : [l.r)にfを作用させる
set(p,x)         : p番目にxを代入
get(p)           : 同じ
prod(l,r)        : 同じ
all_prod()       : 同じ
max_right(p,func): 同じ
min_left(p,func) : 同じ
"""
#セグ木の中身のprint
print([seg.get(i) for i in range()])



[i:i+k] #i番目からk個
range(n-k+1) #iからk個みたいときのfor

bisect_left(x) #x未満の個数
bisect_right(x)#x以下の個数
n - bisect_left(x) #x以上の個数
n - bisect_right(x)#x超過の個数

bisect_left(r) - bisect_left(l)  #L以上R未満の個数
bisect_right(r) - bisect_left(l) #L以上R以下の個数
bisect_left(r) - bisect_right(l) #L超過R未満の個数
bisect_right(r) - bisect_right(l)#L超過R以下の個数

#op = max() のとき
max_right(p,lambda x:x < val)     #p以右で最初にval以上となるindex
max_right(p,lambda x:x <= val)    #p以右で最初にval超過となるindex
min_left(p,lambda x:x < val) - 1  #pより左で最初にval以上となるindex
min_left(p,lambda x:x <= val) - 1 #pより左で最初にval超過となるindex

#op = min() のとき
max_right(p,lambda x:x > val)     #p以右で最初にval以下となるindex
max_right(p,lambda x:x >= val)    #p以右で最初にval未満となるindex
min_left(p,lambda x:x > val) - 1  #pより左で最初にval以下となるindex
min_left(p,lambda x:x >= val) - 1 #pより左で最初にval未満となるindex

#suffix arrayの二分探索
l = bisect.bisect_left(sa,t,key=lambda x:s[x:x+len(t)])
r = bisect.bisect(sa,t,key=lambda x:s[x:x+len(t)])