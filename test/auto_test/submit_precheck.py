import ast

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
        if (
            keyword in problem_spec.problem_statement
            or keyword in problem_spec.output_statement
        ):
            warnings.append(Warning(message))
    return warnings


def check_recursion(code: str) -> list[Warning]:
    tree = ast.parse(code)
    warnings: list[Warning] = []

    class Detector(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node):
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if node.func.id == self.current_function:
                    warnings.append(
                        Warning(
                            f"再帰関数 {self.current_function} が検出されました。再帰上限を調整しましたか？"
                        )
                    )

            elif isinstance(node.func, ast.Attribute):
                if (
                    isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "self"
                    and node.func.attr == self.current_function
                ):
                    warnings.append(
                        Warning(
                            f"再帰関数 {self.current_function} が検出されました。再帰上限を調整しましたか？"
                        )
                    )

            self.generic_visit(node)

    Detector().visit(tree)
    return warnings


def check_all(problem_spec: ProblemSpec, code: str) -> list[Warning]:
    warnings = []

    warnings.extend(check_keywords(problem_spec))
    warnings.extend(check_recursion(code))

    if warnings:
        print(format_text("\n===== 提出前チェック =====", bg=Warning.Color))
        for i, warning in enumerate(warnings, 1):
            print(format_text(f"{i}. {warning}", fg=Warning.Color))

    return warnings
