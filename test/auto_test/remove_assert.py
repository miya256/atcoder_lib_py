import re


def remove_assert(src: str, dst: str) -> None:
    #行の先頭に、空白やタブが0個以上、assert がくる正規表現
    pattern = re.compile(r'^[ \t]*assert\b')

    with open(src, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(dst, "w", encoding="utf-8") as f:
        for line in lines:
            if not pattern.match(line):
                f.write(line)
