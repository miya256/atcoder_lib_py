class CRT:
    def __init__(self, rems=None, mods=None):
        self.rems = rems if rems else []
        self.mods = mods if mods else []
    
    def add(self, rem, mod):
        self.rems.append(rem)
        self.mods.append(mod)
    
    def _extgcd(self,m,n):
        if n == 0:
            return m, 1, 0
        gcd, s, t = self._extgcd(n, m%n)
        return gcd, t, s-(m//n)*t
    
    def _modinv(self, n, mod):
        _,x,_ = self._extgcd(n, mod)
        return x % mod
    
    def _crt(self, rems, mods):
        """2元の場合"""
        gcd, p, _ = self._extgcd(mods[0], mods[1])
        if (rems[1] - rems[0]) % gcd:
            return 0, -1
        m = mods[0] * mods[1] // gcd
        x = (rems[0] + mods[0] * ((rems[1] - rems[0]) * p // gcd % (mods[1] // gcd))) % m
        return x, m
    
    def crt(self):
        """n元"""
        x, m = 0, 1
        for rem, mod in zip(self.rems, self.mods):
            x, m = self._crt((x, rem), (m, mod))
        return x, m
    
    def garner(self, mod=998244353):
        """crtと違い、x % mod の mod はなんでもよい"""
        mods = self.mods
        rems = self.rems
        
        mods.append(mod)
        x = [0] * len(mods) #x[i] = t[0] + t[1]mods[0] + ... + t[k-1]mods[0]mods[1]...mods[k-2]
        m = [1] * len(mods) #m[i] = mods[0]mods[1]...mods[k-1]
        for k in range(len(rems)):
            t = (rems[k] -x[k]) * self._modinv(m[k], mods[k]) % mods[k]
            for i in range(k+1, len(mods)):
                x[i] = (x[i] + t * m[i]) % mods[i]
                m[i] = (m[i] * mods[k]) % mods[i]
        return x[-1]


crt = CRT([2,3],[3,5])
print(crt.garner())