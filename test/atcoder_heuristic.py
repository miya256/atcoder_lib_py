#冒険者が移動するので、木を置いて邪魔する
#花の発見を遅らせたいので、隣のマスに行くまで見えないようにする
#行き止まりにいって戻るをたくさんやらせれば長くなりそう
#行き止まりも曲がるまでわからないほうがいい

#1. 先に迷路をすべて作ってしまう

#2. 移動先に合わせて迷路を構築
#目的地を予想して、そこまで遠回りするように壁をつくる
#このとき、目的地から最も遠いほうに穴をあけておく
#そうすれば、目的地について次のとこにいくとき、来た道を戻らせることができる


from collections import deque,defaultdict,Counter
inf = 1<<61

class Adventurer:
    def __init__(self, n, q):
        self.n = n
        self.x = None
        self.y = None
        self.checked = [[False] * n for _ in range(n)]

        self.q = q #末尾が次の目的地
        self.dst = None

    def check_around(self):
        for dx,dy in (-1,0), (1,0), (0,-1), (0,1):
            k = 1
            while (
                0 <= self.x + k*dx < self.n and
                0 <= self.y + k*dy < self.n and
                b[self.x + k*dx][self.y + k*dy] != "T"
            ):
                self.checked[self.x + k*dx][self.y + k*dy] = True
                k += 1
    
    def reachable(self):
        dq = deque([(self.x, self.y)])
        visited = [[False] * self.n for _ in range(self.n)]
        while dq:
            x, y = dq.popleft()
            if (x, y) == self.dst:
                return True
            if visited[x][y]:
                continue
            visited[x][y] = True
            for dx,dy in (-1,0), (1,0), (0,-1), (0,1):
                nx, ny = x+dx, y+dy
                if not(0 <= nx < self.n and 0 <= ny < self.n):
                    continue
                if b[nx][ny] == "T":
                    continue
                if visited[nx][ny]:
                    continue
                dq.append((nx,ny))
        return False
    
    def decide_dst(self):
        dq = deque([(self.x, self.y)])
        visited = [[False] * self.n for _ in range(self.n)]
        while dq:
            x, y = dq.popleft()
            if visited[x][y]:
                continue
            visited[x][y] = True
            for dx,dy in (-1,0), (1,0), (0,-1), (0,1):
                nx, ny = x+dx, y+dy
                if not(0 <= nx < self.n and 0 <= ny < self.n):
                    continue
                if b[nx][ny] == "T":
                    continue
                if visited[nx][ny]:
                    continue
                dq.append((nx,ny))
        
        while self.q:
            dst = self.q.pop()
            if self.checked[dst[0]][dst[1]]:
                continue
            if not visited[dst[0]][dst[1]]:
                continue
            self.dst = dst
            return
    
    def move(self):
        dq = deque([self.dst + tuple([0])])
        dist = [[inf] * self.n for _ in range(self.n)]
        while dq:
            x, y, d = dq.popleft()
            if dist[x][y] != inf:
                continue
            dist[x][y] = d
            for dx,dy in (-1,0), (1,0), (0,-1), (0,1):
                nx, ny = x+dx, y+dy
                if not(0 <= nx < self.n and 0 <= ny < self.n):
                    continue
                if b[nx][ny] == "T":
                    continue
                if dist[nx][ny] != inf:
                    continue
                dq.append((nx,ny,d+1))
        
        min_ = min(
            dist[self.x+dx][self.y+dy] 
            for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)] 
            if (0 <= self.x+dx < self.n and 0 <= self.y+dy < self.n)
            )
        for dx,dy in (-1,0), (1,0), (0,-1), (0,1):
            if dist[self.x+dx][self.y+dy] == min_:
                self.x += dx
                self.y += dy
                return

    def update(self, is_test):
        if is_test:
            if self.x is None and self.y is None:
                self.x = 0
                self.y = n//2
                self.checked[0][n//2] = True
                return True
            self.check_around()
            if self.checked[ti][tj]: self.dst = (ti, tj)
            if self.dst is not None and not self.reachable(): self.dst = None
            if self.dst is None or (self.dst) != (ti, tj) and self.checked[self.dst[0]][self.dst[1]]: self.decide_dst()
            self.move()
            if self.x == ti and self.y == tj: return False
        else:
            px, py = map(int,input().split())
            if (px, py) == (ti, tj):
                return False
            data = list(map(int,input().split()))
            for i in range(data[0]):
                self.checked[data[i*2+1]][data[i*2+2]] = True
            self.x = px
            self.y = py
        return True

#こちらは目的地がどこなのかはわからない

is_test = True

n, ti, tj = map(int,input().split())
b = [list(input()) for _ in range(n)]
q = [tuple(map(int,input().split())) for _ in range(n*n-1)][::-1] if is_test else None

adventurer = Adventurer(n, q)
while adventurer.update(is_test):
    #確認済みマス、移動を終えているので、その状態でどこに置くか決める
    print(0)
    continue
