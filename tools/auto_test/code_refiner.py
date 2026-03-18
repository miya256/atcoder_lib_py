import ast
import re


class CodeRefiner(ast.NodeTransformer):
    def visit_Assert(self, node):
        """assert文除去"""
        return None

    def visit_Assign(self, node):
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


def refine_code(code: str) -> str:
    tree = ast.parse(code)
    tree = CodeRefiner().visit(tree)
    ast.fix_missing_locations(tree)
    new_code = ast.unparse(tree)
    return new_code
