import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

files = [
    "../library/range_query/segment_tree/segment_tree.py",
    "../library/range_query/fenwick_tree/fenwick_tree.py",
]

def extract_definitions(lines: list[str]) -> tuple[str, str]:
    for line in lines:
        class_match = re.search(r'^class\s+(\w+)', line)
        func_match  = re.search(r'^def\s+(\w+)', line)

        if class_match:
            return "class", class_match.group(1)
        elif func_match:
            return "def", func_match.group(1)


def main():
    snippets = {}
    for path in files:
        full_path = (BASE_DIR / path).resolve()
        with open(full_path, "r", encoding="utf-8") as f:
            lines: list[str] = f.readlines()
        type, name = extract_definitions(lines)
        snippets[name] = {
            "prefix": f"{type} {name}",
            "body": [line.rstrip("\n") for line in lines],
            "description": f"Auto snippet for {name}"
        }
    
    snippets_dir = BASE_DIR / "lib.code-snippets"
    with open(snippets_dir, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()