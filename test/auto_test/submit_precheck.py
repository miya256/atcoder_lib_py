from terminal_formatter import format_text
from parser import ProblemSpec


class Warning:
    Color = "#ff7700"

    def __init__(self, text: str) -> None:
        self.text = text
    
    def __repr__(self):
        return self.text
    

def check_mod(problem_spec: ProblemSpec) -> Warning | None:
    """998244353があるときに警告"""
    if "998244353" in problem_spec.problem_statement:
        return Warning("mod はとりましたか？")

def check_lex_order(problem_spec: ProblemSpec) -> Warning | None:
    """辞書順という言葉があるときに警告"""
    if "辞書順" in problem_spec.problem_statement:
        return Warning("辞書順にしましたか？")

def check_numeric_order(problem_spec: ProblemSpec) -> Warning | None:
    """昇順という言葉があるときに警告"""
    if "昇順" in problem_spec.problem_statement:
        return Warning("昇順にしましたか？")


def check_all(problem_spec: ProblemSpec) -> None:
    warnings = []

    if warning := check_mod(problem_spec):
        warnings.append(warning)
    if warning := check_lex_order(problem_spec):
        warnings.append(warning)
    if warning := check_numeric_order(problem_spec):
        warnings.append(warning)

    if warnings:
        print(format_text("\n===== 提出前チェック =====", bg=Warning.Color))
        for i, warning in enumerate(warnings, 1):
            print(format_text(f"{i}. {warning}", fg=Warning.Color))

    return warnings 