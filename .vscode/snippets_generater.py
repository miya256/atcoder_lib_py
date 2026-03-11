import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

exclude = set([
    "dp/bounded_knapsack.py",
    "graph/directed/scc_tarjan.py",
    "graph/search/bipartite.py",
    "graph/search/dfs.py",
    "math/factor/linear_sieve.py",
    "math/fps/fps.py",
    "math/linear_algebra/matrix_multiple_strassen.py",
    "math/mod/mod_pow.py",
    "math/tools/bit_tricks.py",
    "range_query/sparse_table.py",
    "range_query/fenwick_tree/fenwick_tree_generic.py",
    "split_search/bisect.py",
])

exclude = [Path(path) for path in exclude]

def extract_definitions(lines: list[str]) -> tuple[str, str]:
    for line in lines:
        class_match = re.search(r'^class\s+(\w+)', line)
        func_match  = re.search(r'^def\s+(\w+)', line)

        if class_match:
            return "class", class_match.group(1)
        elif func_match:
            return "def", func_match.group(1)
    raise Exception("no function or class definitions found")


def main():
    snippets = {}
    root = BASE_DIR / "library"
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix != ".py":
            continue
        if path.relative_to(root) in exclude:
            print(f"\033[33mSkip\033[0m {path.relative_to(root)}: listed in exclude")
            continue

        with open(path, "r", encoding="utf-8") as f:
            lines: list[str] = f.readlines()
        try:
            type, name = extract_definitions(lines)
            snippets[name] = {
                "prefix": f"{type} {name}",
                "body": [line.rstrip("\n") for line in lines],
                "description": f"Auto snippet for {name}"
            }
        except Exception as e:
            print(f"\033[33mSkip\033[0m {path.relative_to(root)}: {e}")
    
    snippets_dir = BASE_DIR / ".vscode/lib.code-snippets"
    with open(snippets_dir, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()