from terminal_formatter import format_text
from parser import ProblemSpec


class Warning:
    Color = "#ff7700"

    def __init__(self, text: str) -> None:
        self.text = text
    
    def __repr__(self):
        return self.text
    

def check_keywords(problem_spec: ProblemSpec) -> list[Warning]:
    keywords = {
        "辞書順": "辞書順にしましたか？",
        "昇順": "昇順にしましたか？",
        "降順": "降順にしましたか？",
        "998244353": "mod はとりましたか？",
        "1000000007": "mod はとりましたか？",
    }

    warnings: list[Warning] = []
    for keyword, message in keywords.items():
        if keyword in problem_spec.problem_statement or keyword in problem_spec.output_statement:
            warnings.append(Warning(message))
    return warnings



def check_all(problem_spec: ProblemSpec) -> None:
    warnings = []

    warnings.extend(check_keywords(problem_spec))

    if warnings:
        print(format_text("\n===== 提出前チェック =====", bg=Warning.Color))
        for i, warning in enumerate(warnings, 1):
            print(format_text(f"{i}. {warning}", fg=Warning.Color))

    return warnings 