import ast


class CodeRefiner(ast.NodeTransformer):
    def visit_Assert(self, node):
        """assert文除去"""
        return None


def refine_code(code: str) -> str:
    tree = ast.parse(code)
    tree = CodeRefiner().visit(tree)
    ast.fix_missing_locations(tree)
    new_code = ast.unparse(tree)
    return new_code
