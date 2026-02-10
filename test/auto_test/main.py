import os
import sys
from pathlib import Path

import pyperclip

from terminal_formatter import format_text, SUCCESS_COLOR, ERROR_COLOR

from url_getter import get_current_url
from access import access

from parser import ProblemSpec
from tester import test
import submit_precheck

from code_refiner import refine_code


def print_error(message: str | Exception) -> int:
    print(format_text(message, fg=ERROR_COLOR))
    return 1


def main():
    # atcoderにアクセス -> 開発者ツール -> Aplication -> REVEL_SESSION の値をコピぺ
    # スタート -> 環境変数を編集で検索 -> 開いて編集
    # VSCode を開きなおす（開いたままだと環境変数の更新が反映されないため）
    # 絶対に公開してはいけない
    cookie_value = os.getenv("ATCODER_COOKIE")
    browser = "Edge"
    editor = "Visual Studio Code"
    src_path = Path("./test/atcoder.py")

    # URLを取得
    try:
        url = get_current_url(browser, editor)
    except Exception as e:
        sys.exit(print_error(e))
    if "atcoder.jp" not in url:
        sys.exit(print_error(f"AtCoder の URL を取得できませんでした\nURL: {url}"))

    # ページにアクセス
    try:
        user, html = access(url, cookie_value)
        print(format_text("アクセス成功", fg=SUCCESS_COLOR))
        print(user)
        print(f"URL: {url}\n")
    except Exception as e:
        sys.exit(print_error(f"アクセス失敗\n{e}"))
    
    # 問題文やサンプルをパース
    problem_spec = ProblemSpec(html)
    
    # テスト
    test(src_path, problem_spec)

    # ソースコードを読み込む
    with open(src_path, "r", encoding="utf-8") as f:
        src_lines: list[str] = f.readlines()

    # 提出前チェック
    submit_precheck.check_all(problem_spec)

    # コードを整える（assert文除去など）
    submit_lines = refine_code(src_lines)

    # クリップボードに提出用コードをコピー
    pyperclip.copy(''.join(submit_lines))
    

if __name__ == "__main__":
    main()
