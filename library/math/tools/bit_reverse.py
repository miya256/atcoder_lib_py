#4byte
def bit_reverse(x: int) -> int:
    x = ((x & 0x0000ffff)) << 16 | ((x & 0xffff0000) >> 16)
    x = ((x & 0x00ff00ff)) << 8 | ((x & 0xff00ff00) >> 8)
    x = ((x & 0x0f0f0f0f)) << 4 | ((x & 0xf0f0f0f0) >> 4)
    x = ((x & 0x33333333)) << 2 | ((x & 0xcccccccc) >> 2)
    x = ((x & 0x55555555)) << 1 | ((x & 0xaaaaaaaa) >> 1)
    return x


#8byte
def bit_reverse(x: int) -> int:
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