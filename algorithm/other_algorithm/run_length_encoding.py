#ランレングス圧縮
from itertools import groupby

a = "aaabbbcccckdd"

rle = [(val, len(list(cnt))) for val, cnt in groupby(a)]

print(rle)
