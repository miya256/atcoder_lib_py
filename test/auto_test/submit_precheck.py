from bs4 import BeautifulSoup

from terminal_formatter import format_text


class Warning:
    Color = "#ff7700"

    def __init__(self, text: str) -> None:
        self.text = text
    
    def __repr__(self):
        return self.text
    

def check_mod(problem_statement: str) -> Warning | None:
    """998244353があるときに警告"""
    if "998244353" in problem_statement:
        return Warning("mod はとりましたか？")

def check_lexorder(problem_statement: str) -> Warning | None:
    """辞書順という言葉があるときに警告"""
    if "辞書順" in problem_statement:
        return Warning("辞書順にしましたか？")


def check_all(problem_statement: str) -> None:
    warnings = []

    if warning := check_mod(problem_statement):
        warnings.append(warning)
    if warning := check_lexorder(problem_statement):
        warnings.append(warning)

    if warnings:
        print(format_text("\n===== 提出前チェック =====", bg=Warning.Color))
        for i, warning in enumerate(warnings, 1):
            print(format_text(f"{i}. {warning}", fg=Warning.Color))

    return warnings 