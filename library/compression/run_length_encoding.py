def run_length_encode(a: str | list) -> list[tuple[object, int]]:
    """ランレングス圧縮"""
    rle = []
    l = r = 0
    while l < len(a):
        while r < len(a) and a[l] == a[r]:
            r += 1
        rle.append((a[l], r-l))
        l = r
    return rle