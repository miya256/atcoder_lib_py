x = 0

x & -x #右端の1だけを残す
x & x-1 #右端の1を消す

#int型(4byte)
def bitCount(x):
    x = (x & 0x55555555) + ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = (x & 0x0f0f0f0f) + ((x >> 4) & 0x0f0f0f0f)
    x = (x & 0x00ff00ff) + ((x >> 8) & 0x00ff00ff)
    x = (x & 0x0000ffff) + ((x >> 16) & 0x0000ffff)
    return x

#long型(8byte)
def bitCount(x):
    x = (x & 0x5555555555555555) + ((x >> 1) & 0x5555555555555555)
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    x = (x & 0x0f0f0f0f0f0f0f0f) + ((x >> 4) & 0x0f0f0f0f0f0f0f0f)
    x = (x & 0x00ff00ff00ff00ff) + ((x >> 8) & 0x00ff00ff00ff00ff)
    x = (x & 0x0000ffff0000ffff) + ((x >> 16) & 0x0000ffff0000ffff)
    x = (x & 0x00000000ffffffff) + ((x >> 32) & 0x00000000ffffffff)
    return x

"""例
0b11001011 -> 0b 11 00 10 11　2bitに分けて、それぞれ1の個数にする
0x55555555との&で右側にある1、シフトして&で左にある1を取り出し、足すことで1の個数になる

0b 11 00 10 11
0b 1+1 0+0 0+1 1+1
0b 10 00 01 10 1行目でxはこう変換される


0b 1000 0110 4bitにわけて、1の個数にする
右2つを取り出すには0x33333333と&する。左2つは2回シフトしてから&する

0b 1000 0110
0b 00+10 10+01
0b 0010 0011


0b 00100011 8bitにわける。
4つ取り出すには0x0f0f0f0fと&

0b 0011+0010
0b 00000101
つまり1の数は5
"""

#4byte
def bitReverse():
    x = ((x & 0x0000ffff)) << 16 | ((x & 0xffff0000) >> 16)
    x = ((x & 0x00ff00ff)) << 8 | ((x & 0xff00ff00) >> 8)
    x = ((x & 0x0f0f0f0f)) << 4 | ((x & 0xf0f0f0f0) >> 4)
    x = ((x & 0x33333333)) << 2 | ((x & 0xcccccccc) >> 2)
    x = ((x & 0x55555555)) << 1 | ((x & 0xaaaaaaaa) >> 1)
    return x

#8byte
def bitReverse():
    x = ((x & 0x00000000ffffffff) << 32) | ((x & 0xffffffff00000000) >> 32)
    x = ((x & 0x0000ffff0000ffff) << 16) | ((x & 0xffff0000ffff0000) >> 16)
    x = ((x & 0x00ff00ff00ff00ff) << 8) | ((x & 0xff00ff00ff00ff00) >> 8)
    x = ((x & 0x0f0f0f0f0f0f0f0f) << 4) | ((x & 0x0f0f0f0f0f0f0f0f) >> 4)
    x = ((x & 0x3333333333333333) << 2) | ((x & 0xcccccccccccccccc) >> 2)
    x = ((x & 0x5555555555555555) << 1) | ((x & 0xaaaaaaaaaaaaaaaa) >> 1)
    return x

"""
16bitずつに区切り入れ替えている
8bitずつに区切り、隣合うかたまりをいれかえている
4bitずつに
2
1
"""