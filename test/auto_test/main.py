import os
import sys

from access import access
from url_getter import get_current_url
from terminal_formatter import format_text, SUCCESS_COLOR, ERROR_COLOR
from problem_info_getter import get_time_limit, get_input_samples, get_output_samples, get_problem_statement
from tester import test
from submit_precheck import check_all
from remove_assert import remove_assert
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
        user, soup = access(url, cookie_value)
        print(format_text("アクセス成功", fg=SUCCESS_COLOR))
        print(user)
        print(f"URL: {url}\n")
    except Exception as e:
        sys.exit(print_error(f"アクセス失敗\n{e}"))
    
    # 問題文やサンプルを取得
    try:
        time_limit_s = get_time_limit(soup)
        input_samples = get_input_samples(soup)
        output_samples = get_output_samples(soup)
        problem_statement = get_problem_statement(soup)
    except Exception as e:
        sys.exit(print_error(e))
    
    # テスト
    src = "./test/atcoder.py"
    test(src, time_limit_s, input_samples, output_samples)

    # 提出前チェック
    check_all(problem_statement)

    # assert文除去
    submit = "./test/auto_test/submit.py"
    remove_assert(src, submit)

    # submit.pyの内容をコピー
    copy_code(submit)
    

if __name__ == "__main__":

    main()
