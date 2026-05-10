import libcst as cst
import re
import subprocess

from terminal_formatter import print_error


class CodeRefiner(cst.CSTTransformer):
    def __init__(self):
        # {(module, asname): alias}
        self.import_map: dict[tuple[str, str], cst.ImportAlias] = {}
        # {module: module}
        # {module, {(name, asname): alias}}
        self.from_import_module_map: dict[str, cst.Name | cst.Attribute | None] = {}
        self.from_import_map: dict[str, dict[tuple[str, str], cst.ImportAlias]] = {}
        self.const_map: dict[str, cst.Assign] = {}

    def leave_Assert(self, original_node, updated_node):
        return cst.RemoveFromParent()

    def leave_Assign(self, original_node, updated_node):
        def remove_orig_i(node: cst.Assign):
            """orig_i = i を除去"""
            # 連鎖してない（a=b=1とかじゃない）
            if len(node.targets) > 1:
                return node
            # 左辺は1変数（a,b=1,2とかじゃない）
            if not isinstance(node.targets[0].target, cst.Name):
                return node
            # 右辺も変数
            if not isinstance(node.value, cst.Name):
                return node

            var_name: str = node.targets[0].target.value
            if match := re.fullmatch(r"orig_(.)", var_name):
                if match.group(1) == node.value.value:
                    return None
            return node

        def remove_duplicate_const(node: cst.Assign):
            """重複定数除去"""
            # 連鎖してない（a=b=1とかじゃない）
            if len(node.targets) > 1:
                return node
            # 左辺は1変数（a,b=1,2とかじゃない）
            if not isinstance(node.targets[0].target, cst.Name):
                return node

            name = node.targets[0].target.value
            if name in ("inf", "mod"):
                self.const_map[name] = node
                return None
            return node

        node = remove_orig_i(updated_node)
        if node is None:
            return cst.RemoveFromParent()

        node = remove_duplicate_const(node)
        if node is None:
            return cst.RemoveFromParent()

        return node

    def leave_Import(self, original_node, updated_node):
        for alias in updated_node.names:
            module = self._module(alias.name)
            if alias.asname is None:
                asname = ""
            else:
                assert isinstance(alias.asname.name, cst.Name)
                asname = alias.asname.name.value
            self.import_map[(module, asname)] = alias
        return cst.RemoveFromParent()

    def leave_ImportFrom(self, original_node, updated_node):
        module = self._module(updated_node.module)
        self.from_import_module_map[module] = updated_node.module

        assert not isinstance(updated_node.names, cst.ImportStar)
        for alias in updated_node.names:
            assert isinstance(alias.name, cst.Name)
            alias.name.value
            if alias.asname is None:
                asname = ""
            else:
                assert isinstance(alias.asname.name, cst.Name)
                asname = alias.asname.name.value
            self.from_import_map.setdefault(module, {})[(alias.name.value, asname)] = (
                alias
            )
        return cst.RemoveFromParent()

    def leave_Module(self, original_node, updated_node):
        import_list = [
            cst.SimpleStatementLine([cst.Import(names=[alias])])
            for alias in self.import_map.values()
        ]
        from_import_list = [
            cst.SimpleStatementLine(
                [
                    cst.ImportFrom(
                        module=self.from_import_module_map[module],
                        names=list(self.from_import_map[module].values()),
                    )
                ]
            )
            for module in self.from_import_map.keys()
        ]
        const_list = [
            cst.SimpleStatementLine([assign]) for assign in self.const_map.values()
        ]
        new_body = import_list + from_import_list + const_list + list(updated_node.body)
        return updated_node.with_changes(body=new_body)

    def _module(self, value: cst.Name | cst.Attribute | None) -> str:
        if value is None:
            return ""
        if isinstance(value, cst.Name):
            return value.value
        assert isinstance(value.value, cst.Name | cst.Attribute)
        return f"{self._module(value.value)}.{value.attr.value}"


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


def refine_code_v2(code: str) -> str:
    code = format_code(code)
    tree = cst.parse_module(code)
    tree = tree.visit(CodeRefiner())
    new_code = format_code(tree.code)
    return new_code
