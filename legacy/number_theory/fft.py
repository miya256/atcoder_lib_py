import numpy as np

class FFT:
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
        x = np.array(x, dtype=np.complex128)
        n = len(x) >> 1
        while n:
            for i in range(n):
                w = np.cos(i * np.pi / n) - 1j * np.sin(i * np.pi / n)
                x[i::n*2], x[i+n::n*2] = x[i::n*2] + x[i+n::n*2], w * (x[i::n*2] - x[i+n::n*2])
            n >>= 1
        return x

    def dit(self,x):
        x = np.array(x, dtype=np.complex128)
        n = 1
        while n < len(x):
            for i in range(n):
                w = np.cos(i * np.pi / n) + 1j * np.sin(i * np.pi / n)
                x[i::n*2], x[i+n::n*2] = x[i::n*2] + w * x[i+n::n*2], x[i::n*2] - w * x[i+n::n*2]
            n <<= 1
        return x / n
    
    def fft(self,x):
        x = self.dif(x)
        self.bitReverseSort(x)
        return x
    
    def ifft(self,x):
        self.bitReverseSort(x)
        x = self.dit(x)
        return x
    
    def convolution(self,a,b):
        n = 1 << (len(a) + len(b) - 2).bit_length()
        a += [0] * (n - len(a))
        b += [0] * (n - len(b))
        c = self.dit(self.dif(a) * self.dif(b))
        return c

fft = FFT()
n,m = map(int,input().split())
a = list(map(int,input().split()))
b = list(map(int,input().split()))

c = fft.convolution(a,b)

for i in range(n+m-1):
    print(c[i])