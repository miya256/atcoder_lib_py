class NTT:
    MOD = 998244353 # = 119 * 2^23 + 1
    W = 31 #2^23乗根 g^(119*2^23/N) = (g^119)^(2^23/N) で、g^119 = 31 が最小ぽい？
    M = 23

    def __init__(self):
        self.w = [0] * self.M + [self.W] #2^i乗根
        self.iw = [0] * self.M + [pow(self.W, self.MOD-2, self.MOD)]
        for i in range(self.M,0,-1):
            self.w[i-1] = (self.w[i] * self.w[i]) % self.MOD
            self.iw[i-1] = (self.iw[i] * self.iw[i]) % self.MOD
    
    def bitReverse(self,x):
        x = ((x & 0x0000ffff)) << 16 | ((x & 0xffff0000) >> 16)
        x = ((x & 0x00ff00ff)) << 8 | ((x & 0xff00ff00) >> 8)
        x = ((x & 0x0f0f0f0f)) << 4 | ((x & 0xf0f0f0f0) >> 4)
        x = ((x & 0x33333333)) << 2 | ((x & 0xcccccccc) >> 2)
        x = ((x & 0x55555555)) << 1 | ((x & 0xaaaaaaaa) >> 1)
        return x
    
    def bitReverseSort(self,x):
        shift = 32 - len(x).bit_count()
        for i in range(len(x)):
            j = self.bitReverse(i) >> shift
            if i < j:
                x[i], x[j] = x[j], x[i]
    
    def dif(self,x):
        n = len(x) >> 1
        for i in range(n.bit_length(),0,-1):
            for j in range(0,len(x),n*2):
                w = 1
                for k in range(n):
                    s = x[j+k]
                    t = x[j+k+n]
                    x[j+k] = (s + t) % self.MOD
                    x[j+k+n] = w * (s - t) % self.MOD
                    w = (w * self.w[i]) % self.MOD
            n >>= 1
        return x
    
    def dit(self,x):
        n = 1
        for i in range(1,len(x).bit_length()):
            for j in range(0,len(x),n*2):
                w = 1
                for k in range(n):
                    s = x[j+k]
                    t = x[j+k+n]
                    x[j+k] = (s + w * t) % self.MOD
                    x[j+k+n] = (s - w * t) % self.MOD
                    w = (w * self.iw[i]) % self.MOD
            n <<= 1
        invn = pow(n,self.MOD-2,self.MOD)
        x = [xi * invn % self.MOD for xi in x]
        return x
    
    def ntt(self,x):
        x = self.dif(x)
        self.bitReverseSort(x)
        return x
    
    def intt(self,x):
        self.bitReverseSort(x)
        x = self.dit(x)
        return x
    
    def convolution(self,a,b):
        a, b = list(a), list(b)
        n = 1 << (len(a) + len(b) - 2).bit_length()
        a += [0] * (n - len(a))
        b += [0] * (n - len(b))
        c = self.dit([i * j % self.MOD for i,j in zip(self.dif(a),self.dif(b))])
        return c


ntt = NTT()
n,m = map(int,input().split())
a = list(map(int,input().split()))
b = list(map(int,input().split()))

c = ntt.convolution(a,b)

for i in range(n+m-1):
    print(c[i])