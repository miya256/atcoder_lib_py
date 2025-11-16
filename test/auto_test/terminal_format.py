class Style:
    Reset = 0 # 色もすべてリセット
    Bold = 1 #太字
    Italic = 3 # 斜体
    Underline = 4 # 下線
    Strikethrough = 9 # 打消し線


#背景色、文字のスタイルも変えられるらしい

def format_text(
        text,
        *,
        fg: int | None = None,
        bg: int | None = None,
        style: int | None = None
    ):
    """
    ターミナルに表示する文字のフォーマット
    色は24bit 16進文字列で
    """
    codes = []
    mask = (1 << 8) - 1

    if style is not None:
        codes.append(str(style))
    if fg is not None:
        codes.extend(["38", "2", str(int(fg[1:3], 16)), str(int(fg[3:5], 16)), str(int(fg[5:7], 16))])
    if bg is not None:
        codes.extend(["48", "2", str(int(bg[1:3], 16)), str(int(bg[3:5], 16)), str(int(bg[5:7], 16))])

    if codes:
        return f"\033[{';'.join(codes)}m{text}\033[0m"
    else:
        return text