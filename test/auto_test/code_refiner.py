import re


def remove_assert(src_lines: list[str]) -> list[str]:
    """assert文を取り除く"""
    # 行の先頭に、空白やタブが0個以上、assert がくる正規表現
    pattern = re.compile(r"^[ \t]*assert\b")
    return [line for line in src_lines if not pattern.match(line)]


def remove_type_hints(src_lines: list[str]) -> list[str]:
    """型ヒントを取り除く"""
    return src_lines


def remove_unused_imports(src_lines: list[str]) -> list[str]:
    """不要なimportを取り除く"""
    return src_lines


def refine_code(src_lines: list[str]) -> list[str]:
    src_lines = remove_assert(src_lines)
    return src_lines
