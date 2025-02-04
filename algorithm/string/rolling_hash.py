#文字列を逆にしたhashが欲しかったら逆のやつもつくればよい
#s[l:r)の逆は、rev(s)[len-r:len-l)
import random

class RollingHash:
    Mod = (1 << 61) - 1
    Mask30 = (1 << 30) - 1
    Mask31 = (1 << 31) - 1
    Mask61 = Mod
    base = 0
    basePow = [1]#base**i
    
    def __init__(self,s):
        self.s = s
        if RollingHash.base == 0:
            RollingHash.base = random.randrange(1 << 31, RollingHash.Mod)
        if len(RollingHash.basePow) <= len(s):
            self._makeBasePow(len(s))
        self.hash = [1]
        for t in s:
            self.hash.append(self._calcMod(self._mul(self.hash[-1],RollingHash.base) + ord(t)))
    
    def __getitem__(self,i):
        return self.s[i]

    def gethash(self,l,r):
        """[l,r)"""
        res = self.hash[r] - self._mul(self.hash[l], RollingHash.basePow[r-l])
        return res if res >= 0 else res + RollingHash.Mod
    
    def join(self,hash_s,hash_t,len_s):
        """s,tを結合した文字列のhash値"""
        return ((hash_s * RollingHash.basePow[len_s]) % RollingHash.Mod + hash_t) % RollingHash.Mod
    
    def _calcMod(self,x):
        xu, xd = x >> 61, x & RollingHash.Mask61
        res = xu + xd
        return res if res < RollingHash.Mod else res - RollingHash.Mod

    def _mul(self,a,b):
        au, ad = a >> 31, a & RollingHash.Mask31
        bu, bd = b >> 31, b & RollingHash.Mask31
        mid = ad * bu + au * bd
        midu, midd = mid >> 30, mid & RollingHash.Mask30
        return self._calcMod(au * bu * 2 + midu + (midd << 31) + ad * bd)

    def _makeBasePow(self,x):
        l = len(RollingHash.basePow)
        for _ in range(x - l + 1):
            RollingHash.basePow.append(self._mul(RollingHash.base, RollingHash.basePow[-1]))

h = RollingHash("abcdefg")
print(h[0:5:2])
#ace