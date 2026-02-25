import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import pyperclip

from terminal_formatter import (
    format_text,
    print_error,
    SUCCESS_COLOR,
)

from url_getter import get_current_url
from access import access

from parser import ProblemSpec
from tester import test
import submit_precheck

from code_refiner import refine_code


def main():
    load_dotenv()  # .envを読む（ただし既存環境変数は上書きしない）

    cookie_value = os.getenv("ATCODER_REVEL_SESSION")
    if cookie_value is None:
        print_error("ATCODER_REVEL_SESSION の値を設定してください")
        return 1
    browser = os.getenv("BROWSER", "Edge")
    editor = os.getenv("EDITOR", "Visual Studio Code")
    src_path = Path(os.getenv("SRC_PATH", "./test/atcoder.py"))

    # URLを取得
    try:
        url = get_current_url(browser, editor)
    except Exception as e:
        print_error(e)
        return 1
    if "atcoder.jp" not in url:
        print_error(f"AtCoder の URL を取得できませんでした\nURL: {url}")
        return 1

    # ページにアクセス
    try:
        user, html = access(url, cookie_value)
        print(format_text("アクセス成功", fg=SUCCESS_COLOR))
        print(user)
        print(f"URL: {url}\n")
    except Exception as e:
        print_error(f"アクセス失敗\n{e}")
        return 1
    
    # 問題文やサンプルをパース
    problem_spec = ProblemSpec(html)
    
    # テスト
    test(src_path, problem_spec)

    # ソースコードを読み込む
    with open(src_path, "r", encoding="utf-8") as f:
        src_lines: list[str] = f.readlines()

    # 提出前チェック
    submit_precheck.check_all(problem_spec, src_lines)

    # コードを整える（assert文除去など）
    submit_lines = refine_code(src_lines)

    # クリップボードに提出用コードをコピー
    pyperclip.copy(''.join(submit_lines))
    

if __name__ == "__main__":
    main()
