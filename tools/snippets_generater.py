import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

exclude = {
    "dp/bounded_knapsack.py",
    "graph/directed/scc_tarjan.py",
    "graph/search/dfs.py",
    "math/factor/linear_sieve.py",
    "math/fps/fps.py",
    "math/linear_algebra/matrix_multiple_strassen.py",
    "math/mod/mod_pow.py",
    "math/tools/bit_tricks.py",
    "range_query/fenwick_tree/fenwick_tree_generic.py",
}

exclude_imports = {
    "library.graph.graph",
    "library.math.linear_algebra.matrix",
    "library.connectivity.union_find",
    "library.geometry.point",
}

exclude = [Path(path) for path in exclude]


class CodeRefiner(ast.NodeTransformer):
    def visit_ImportFrom(self, node):
        if node.module in exclude_imports:
            return None
        return node


def add_snippets(snippets: dict, path: Path) -> None:
    if path.relative_to(ROOT / "library") in exclude:
        raise Exception("listed in exclude")

    with open(path, "r", encoding="utf-8") as f:
        code: str = f.read()

    tree = ast.parse(code)

    top_classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    top_functions = [
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    ]
    if top_classes:
        def_type, name = "class", top_classes[0]
    elif top_functions:
        def_type, name = "def", top_functions[0]
    else:
        raise Exception("no function or class definitions found")

    refiner = CodeRefiner()
    tree = refiner.visit(tree)
    ast.fix_missing_locations(tree)
    new_code = ast.unparse(tree)

    snippets[name] = {
        "prefix": f"{def_type} {name}",
        "body": [line.rstrip("\n") for line in new_code.splitlines()] + ["$0"],
        "description": f"Auto snippet for {name}",
    }


def main():
    snippets = {}
    library_path = ROOT / "library"
    for path in sorted(library_path.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix != ".py":
            continue

        try:
            add_snippets(snippets, path)
        except Exception as e:
            print(f"\033[33mSkip\033[0m {path.relative_to(library_path)}: {e}")

    snippets_dir = ROOT / ".vscode/lib.code-snippets"
    with open(snippets_dir, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
