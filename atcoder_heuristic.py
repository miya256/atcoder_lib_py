"""
50*50の区画に、線路、駅を設置
線路は2方向と接続できる。あとで駅に置き換えられる。100減る
駅は、４方向と接続できる。5000減る

人cは、家と職場と駅の距離が2以下で線路がつながっているなら、
家と職場のマンハッタン距離だけ払う
"""
"""
はじめは資金を集めたいから、距離が近いやつを繋げる。
駅は家と職場を合わせて複数の地点を含められるところがいい。
線路を交差させたい場合は駅を設置

家と職場の近くに駅がある
できるだけ近くの駅まで移動してから線路を敷く

どちらかに駅がある
駅がないほうにはできるだけ地点を含む場所に駅をつくる
すでに駅があるほうから、できるだけ目的地に近づいてから線路を敷く
"""
STATION = 0
RAIL_HORIZONTAL = 1
RAIL_VERTICAL = 2
RAIL_LEFT_DOWN = 3
RAIL_LEFT_UP = 4
RAIL_RIGHT_UP = 5
RAIL_RIGHT_DOWN = 6
COST_STATION = 5000
COST_RAIL = 100

class Person:
    def __init__(self,si,sj,ti,tj):
        self.si = si #家の座標
        self.sj = sj
        self.ti = ti #職場の座標
        self.tj = tj
        self.has_station_s = False #家から2以下の範囲に駅があるか
        self.has_station_t = False #職場から2以下の範囲に駅があるか
        self.merged = False #家と職場が線路でつながれているか
    
    def dist(self):
        return abs(self.si - self.ti) + abs(self.sj - self.tj)

class Grid:
    def __init__(self,n):
        self.g = [[-1]*n for _ in range(n)]

def build(type,i,j):
    global k,t
    print(type,i,j)
    k -= 5000 if type == 0 else 100
    t -= 1

def merge(src,dest):
    if src[0] < dest[0]:
        for i in range(src[0]+1,dest[0]):
            build(RAIL_VERTICAL,i,src[1])
        if src[1] < dest[1]:
            build(RAIL_RIGHT_UP,dest[0],src[1])
        elif src[1] > dest[1]:
            build(RAIL_RIGHT_UP,dest[0],src[1])
    elif src[0] > dest[0]:
        for i in range(dest[0]+1,src[0]):
            build(RAIL_VERTICAL,i,src[1])
        if src[1] < dest[1]:
            build(RAIL_RIGHT_DOWN,dest[0],src[1])
        elif src[1] > dest[1]:
            build(RAIL_LEFT_DOWN,dest[0],src[1])
    if src[1] < dest[1]:
        for j in range(src[1]+1,dest[1]):
            build(RAIL_HORIZONTAL,dest[0],j)
    elif src[1] > dest[1]:
        for j in range(dest[1]+1,src[1]):
            build(RAIL_HORIZONTAL,dest[0],j)


def merge1(): #距離が一番近いやつを繋げる
    p = min(persons,key=lambda x:x.dist())
    src,dest = (-1,-1),(-1,-1)
    cnt = 0
    for di_s in range(-2,3):
        for dj_s in range(-2+abs(di_s),3-abs(di_s)):
            for di_t in range(-2,3):
                for dj_t in range(-2+abs(di_t),3-abs(di_t)):
                    ni_s, nj_s = p.si+di_s, p.sj+dj_s
                    ni_t, nj_t = p.ti+di_t, p.tj+dj_t
                    if not(0<=ni_s<n and 0<=nj_s<n and 0<=ni_t<n and 0<=nj_t<n):
                        continue
                    if (abs(ni_s-ni_t)+abs(nj_s-nj_t)-1)*100 + 10000 > k:
                        continue
                    tmp = 0
                    for di in range(-2,3):
                        for dj in range(-2+abs(di),3-abs(di)):
                            ni,nj = ni_s+di,nj_s+dj
                            if (ni,nj) in s:
                                tmp += 1
                    for di in range(-2,3):
                        for dj in range(-2+abs(di),3-abs(di)):
                            ni,nj = ni_t+di,nj_t+dj
                            if (ni,nj) in s:
                                tmp += 1
                    if tmp > cnt:
                        cnt = tmp
                        src = (ni_s,nj_s)
                        dest = (ni_t,nj_t)
    build(STATION,src[0],src[1])
    build(STATION,dest[0],dest[1])
    merge(src,dest)
    return src,dest
        
    

n,m,k,t = map(int,input().split()) #n*n、m人、初期資金、ターン数
persons = [Person(*map(int,input().split())) for _ in range(m)]
s = set() #座標たち
for p in persons:
    s.add((p.si,p.sj))
    s.add((p.ti,p.tj))
src,dest = merge1()

level = [set() for _ in range(4)]

while t:
    print(-1)
    t -= 1