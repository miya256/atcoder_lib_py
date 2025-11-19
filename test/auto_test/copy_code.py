import pyperclip


def copy_code(src: str) -> None:
    """クリップボードにコードをコピー"""
    with open(src, "r", encoding="utf-8") as f:
        code = f.read()
    pyperclip.copy(code)