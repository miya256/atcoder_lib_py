class Style:
    Reset = 0 # 色もすべてリセット
    Bold = 1 #太字
    Italic = 3 # 斜体
    Underline = 4 # 下線
    Strikethrough = 9 # 打消し線


ERROR_COLOR = "#dd0000"
SUCCESS_COLOR = "#00ff00"


def format_text(
        text,
        *,
        fg: str | None = None,
        bg: str | None = None,
        styles: list[int] | None = None
    ) -> str:
    """
    ターミナルに表示する文字のフォーマット
    色は24bit 16進文字列で
    """
    codes = []

    if styles is not None:
        for style in styles:
            codes.append(str(style))
    if fg is not None:
        codes.extend(["38", "2", str(int(fg[1:3], 16)), str(int(fg[3:5], 16)), str(int(fg[5:7], 16))])
    if bg is not None:
        codes.extend(["48", "2", str(int(bg[1:3], 16)), str(int(bg[3:5], 16)), str(int(bg[5:7], 16))])

    if codes:
        return f"\033[{';'.join(codes)}m{text}\033[0m"
    else:
        return text