# 4byte
def bit_reverse_32(x: int) -> int:
    x = (x & 0x0000FFFF) << 16 | ((x & 0xFFFF0000) >> 16)
    x = (x & 0x00FF00FF) << 8 | ((x & 0xFF00FF00) >> 8)
    x = (x & 0x0F0F0F0F) << 4 | ((x & 0xF0F0F0F0) >> 4)
    x = (x & 0x33333333) << 2 | ((x & 0xCCCCCCCC) >> 2)
    x = (x & 0x55555555) << 1 | ((x & 0xAAAAAAAA) >> 1)
    return x


# 8byte
def bit_reverse_64(x: int) -> int:
    x = ((x & 0x00000000FFFFFFFF) << 32) | ((x & 0xFFFFFFFF00000000) >> 32)
    x = ((x & 0x0000FFFF0000FFFF) << 16) | ((x & 0xFFFF0000FFFF0000) >> 16)
    x = ((x & 0x00FF00FF00FF00FF) << 8) | ((x & 0xFF00FF00FF00FF00) >> 8)
    x = ((x & 0x0F0F0F0F0F0F0F0F) << 4) | ((x & 0x0F0F0F0F0F0F0F0F) >> 4)
    x = ((x & 0x3333333333333333) << 2) | ((x & 0xCCCCCCCCCCCCCCCC) >> 2)
    x = ((x & 0x5555555555555555) << 1) | ((x & 0xAAAAAAAAAAAAAAAA) >> 1)
    return x


"""
16bitずつに区切り入れ替えている
8bitずつに区切り、隣合うかたまりをいれかえている
4bitずつに
2
1
"""
