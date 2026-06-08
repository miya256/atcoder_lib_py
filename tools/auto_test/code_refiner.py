import ast
import re
import subprocess

from terminal_formatter import print_error


class CodeRefiner(ast.NodeTransformer):
    def __init__(self):
        self.import_set: set[tuple[str, str | None]] = set()
        self.from_import_map: dict[
            tuple[str | None, int], set[tuple[str, str | None]]
        ] = {}
        self.const_set: set[tuple[str, str]] = set()

    def visit_Assert(self, node):
        """assert文除去"""
        return None

    def visit_Assign(self, node):
        def remove_orig_i(node):
            """orig_i = i を除去"""
            if len(node.targets) > 1:
                return node
            if not isinstance(node.targets[0], ast.Name):
                return node
            if not isinstance(node.value, ast.Name):
                return node
            var_name: str = node.targets[0].id
            if match := re.fullmatch(r"orig_(.)", var_name):
                if match.group(1) == node.value.id:
                    return None
            return node

        def remove_duplicate_const(node):
            """重複inf除去"""
            if node is None:
                return None
            if len(node.targets) > 1:
                return node
            if not isinstance(node.targets[0], ast.Name):
                return node
            name = node.targets[0].id
            if name == "inf":
                value = ast.unparse(node.value)
                self.const_set.add((name, value))
                return None
            return node

        node = remove_orig_i(node)
        node = remove_duplicate_const(node)
        return node

    def visit_Import(self, node):
        for alias in node.names:
            self.import_set.add((alias.name, alias.asname))
        return None

    def visit_ImportFrom(self, node):
        k = (node.module, node.level)
        self.from_import_map.setdefault(k, set())
        for alias in node.names:
            self.from_import_map[k].add((alias.name, alias.asname))
        return None


def format_code(code: str) -> str:
    try:
        result = subprocess.run(
            ["uv", "run", "ruff", "format", "-"],
            input=code,
            text=True,
            capture_output=True,
            check=True,
            encoding="utf-8",
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print_error(f"コードのフォーマット中に問題が発生しました:\n{e.stderr}")
        return ""


def refine_code(code: str) -> str:
    refiner = CodeRefiner()
    tree = ast.parse(code)
    tree = refiner.visit(tree)

    imports = [
        ast.Import(names=[ast.alias(name, asname)])
        for name, asname in refiner.import_set
    ]
    from_imports = [
        ast.ImportFrom(
            module=module,
            names=[ast.alias(name, asname) for name, asname in names],
            level=level,
        )
        for (module, level), names in refiner.from_import_map.items()
    ]
    consts = [
        ast.Assign(
            targets=[ast.Name(id=name, ctx=ast.Store())],
            value=ast.parse(value, mode="eval").body,
        )
        for name, value in refiner.const_set
    ]

    tree.body = imports + from_imports + consts + tree.body
    ast.fix_missing_locations(tree)
    new_code = ast.unparse(tree)
    new_code = format_code(new_code)
    return new_code
