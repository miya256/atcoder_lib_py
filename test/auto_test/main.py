import os
import sys

from terminal_formatter import format_text, SUCCESS_COLOR, ERROR_COLOR

from url_getter import get_current_url
from access import access

from parser import ProblemSpec
from tester import test
from submit_precheck import check_all

from code_refiner import refine_code
from copy_code import copy_code


def print_error(message: str | Exception) -> int:
    print(format_text(message, fg=ERROR_COLOR))
    return 1


def main():
    # atcoderにアクセス -> 開発者ツール -> Aplication -> REVEL_SESSION の値をコピぺ
    # スタート -> 環境変数を編集で検索 -> 開いて編集
    # VSCode を開きなおす（開いたままだと環境変数の更新が反映されないため）
    # 絶対に公開してはいけない
    cookie_value = os.getenv("ATCODER_COOKIE")

    # URLを取得
    try:
        url = get_current_url("Edge", "Visual Studio Code")
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
    src = "./test/atcoder.py"
    test(src, problem_spec)

    # 提出前チェック
    check_all(problem_spec)

    # コードを整える（assert文除去など）
    submit = "./test/auto_test/submit.py"
    refine_code(src, submit)

    # submit.pyの内容をコピー
    copy_code(submit)
    

if __name__ == "__main__":
    main()
