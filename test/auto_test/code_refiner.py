import ast


class CodeRefiner(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        """関数のアノテーション除去"""
        # 引数の型削除
        for arg in node.args.args:
            arg.annotation = None

        for arg in node.args.kwonlyargs:
            arg.annotation = None

        if node.args.vararg:
            node.args.vararg.annotation = None

        if node.args.kwarg:
            node.args.kwarg.annotation = None

        # 戻り値削除
        node.returns = None

        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        """変数のアノテーション除去"""
        if node.value is None:
            return None
        return ast.Assign(targets=[node.target], value=node.value)

    def visit_ImportFrom(self, node):
        """typing import除去"""
        if node.module == "typing":
            return None
        return node

    def visit_Assert(self, node):
        """assert文除去"""
        return None


def refine_code(code: str) -> str:
    tree = ast.parse(code)
    tree = CodeRefiner().visit(tree)
    ast.fix_missing_locations(tree)
    new_code = ast.unparse(tree)
    return new_code
