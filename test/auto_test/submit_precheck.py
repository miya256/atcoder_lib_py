import re

from terminal_formatter import format_text
from parser import ProblemSpec


class Warning:
    Color = "#ff7700"

    def __init__(self, text: str) -> None:
        self.text = text
    
    def __repr__(self):
        return self.text
    

def check_keywords(problem_spec: ProblemSpec) -> list[Warning]:
    """問題文にキーワードが含まれているか確認する"""
    keywords = {
        "辞書順": "辞書順にしましたか？",
        "昇順": "昇順にしましたか？",
        "降順": "降順にしましたか？",
        "998244353": "mod はとりましたか？",
        "1000000007": "mod はとりましたか？",
    }

    if problem_spec.problem_statement is None:
        return []
    if problem_spec.output_statement is None:
        return []

    warnings: list[Warning] = []
    for keyword, message in keywords.items():
        if keyword in problem_spec.problem_statement or keyword in problem_spec.output_statement:
            warnings.append(Warning(message))
    return warnings


def check_recursion(src_lines: list[str]) -> list[Warning]:
    """ソースコードに再帰構造があるか確認する"""
    warnings: list[Warning] = []
    INDENT = 4
    func_pattern = re.compile(r"^\s*def\s+(\w+)\s*\(")
    func_stack: list[tuple[str, int]] = [("DUMMY_FUNC", -1)] # (関数名, ネストの深さ)
    for line in src_lines:
        if line.strip() == "":
            continue

        nests = (len(line) - len(line.lstrip(" "))) // INDENT
        while func_stack and func_stack[-1][1] >= nests:
            func_stack.pop()
        
        call_pattern = re.compile(rf"\b{func_stack[-1][0]}\s*\(")
        if call_pattern.search(line):
            warnings.append(Warning(
                f"再帰関数 {func_stack[-1][0]} が検出されました。再帰上限を調整しましたか？"
            ))
        if match := func_pattern.match(line):
            func_name = match.group(1)
            func_stack.append((func_name, nests))

    return warnings


def check_all(problem_spec: ProblemSpec, src_lines: list[str]) -> None:
    warnings = []

    warnings.extend(check_keywords(problem_spec))
    warnings.extend(check_recursion(src_lines))

    if warnings:
        print(format_text("\n===== 提出前チェック =====", bg=Warning.Color))
        for i, warning in enumerate(warnings, 1):
            print(format_text(f"{i}. {warning}", fg=Warning.Color))

    return warnings 