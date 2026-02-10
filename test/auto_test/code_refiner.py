import re


def remove_assert(src_lines: list[str]) -> list[str]:
    """assert文を取り除く"""
    #行の先頭に、空白やタブが0個以上、assert がくる正規表現
    pattern = re.compile(r'^[ \t]*assert\b')
    return [line for line in src_lines if not pattern.match(line)]


def refine_code(src_lines: list[str]) -> list[str]:
    src_lines = remove_assert(src_lines)
    return src_lines