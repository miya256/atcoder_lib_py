import random

class RollingHash:
    """
    hashを比較することで文字の一致判定

    Methods:
        hash(l, r)         : [l, r)のhash。__call__でも呼べる
        join(sh, th)       : s,tをこの順に結合した文字列のhash値
        is_palindrome(l, r): [l, r)が回文か
        make_reverse()     : 逆向きのインスタンスを生成
    """

    MOD = (1 << 61) - 1
    MASK30 = (1 << 30) - 1
    MASK31 = (1 << 31) - 1
    MASK61 = MOD
    base = None
    base_pow = [1]

    def __init__(self, string: str) -> None:
        self.string = string
        if RollingHash.base is None:
            RollingHash.base = random.randrange(1 << 31, RollingHash.MOD)
        if len(RollingHash.base_pow) <= len(string):
            self._make_base_pow(len(string))
        self._hash = [1]
        for char in string:
            self._hash.append(self._calc_mod(self._mul(self._hash[-1], RollingHash.base) + ord(char)))
    
    def __len__(self) -> int:
        return len(self.string)
    
    def __getitem__(self, i: int) -> str:
        return self.string[i]
    
    def __call__(self, l: int, r: int) -> int:
        """[l,r)のhash"""
        return self.hash(l, r)
    
    def hash(self, l: int, r: int) -> int:
        """[l,r)のhash"""
        assert 0 <= l <= r <= len(self), f"index error [l,r)=[{l},{r})"
        res = self._hash[r] - self._mul(self._hash[l], RollingHash.base_pow[r-l])
        return res if res >= 0 else res + RollingHash.MOD
    
    def is_palindrome(self, l: int, r: int) -> bool:
        """[l, r)が回文か"""
        assert 0 <= l <= r <= len(self), f"index error [l,r)=[{l},{r})"
        self.make_reverse()
        return self(l, r) == self._rev_hash(len(self)-r, len(self)-l)
    
    def make_reverse(self) -> "RollingHash":
        """逆向きのインスタンスを生成"""
        if not hasattr(self, "_rev_hash"):
            self._rev_hash = RollingHash(self.string[::-1])
        return self._rev_hash
    
    def _calc_mod(self, x: int) -> int:
        xu, xd = x >> 61, x & RollingHash.MASK61
        res = xu + xd
        return res if res < RollingHash.MOD else res - RollingHash.MOD

    def _mul(self, a: int, b: int) -> int:
        au, ad = a >> 31, a & RollingHash.MASK31
        bu, bd = b >> 31, b & RollingHash.MASK31
        mid = ad * bu + au * bd
        midu, midd = mid >> 30, mid & RollingHash.MASK30
        return self._calc_mod(au * bu * 2 + midu + (midd << 31) + ad * bd)
    
    def _make_base_pow(self, x: int) -> None:
        l = len(RollingHash.base_pow)
        for _ in range(x - l + 1):
            RollingHash.base_pow.append(self._mul(RollingHash.base, RollingHash.base_pow[-1]))
    
    @staticmethod
    def join(hash_s: int, hash_t: int, len_t: int) -> int:
        """s,tをこの順に結合した文字列のhash値"""
        return ((hash_s * RollingHash.base_pow[len_t]) % RollingHash.MOD + hash_t) % RollingHash.MOD
    