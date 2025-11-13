def kmp(text: str, pattern: str) -> int:
    """textからpatternを検索。O(n)"""
    def createTable(pattern: str) -> list[int]:
        """何個戻るかを計算"""
        table = [0] * len(pattern)
        table[0] = -1
        j = -1
        for i in range(len(pattern)-1):
            while j >= 0 and pattern[i] != pattern[j]:
                j = table[j]
            table[i+1] = j+1
            j += 1
        return table
    
    table = createTable(pattern)
    i = j = 0
    while i+j < len(text):
        if text[i+j] == pattern[j]:
            j += 1
            if j == len(pattern):
                return i
        else:
            i = i + j - table[j]
            if j > 0:
                j = table[j]
    return -1