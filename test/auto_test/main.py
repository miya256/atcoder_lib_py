import os

from access import access
from terminal_formatter import format_text, SUCCESS_COLOR, ERROR_COLOR
from problem_info import get_time_limit, get_input_samples, get_output_samples, get_problem_statement
from tester import test
from submit_precheck import check_all


def main():
    url = "https://atcoder.jp/contests/abc431/tasks/abc431_f"

    # atcoderにアクセス -> 開発者ツール -> Aplication -> REVEL_SESSION の値をコピぺ
    # スタート -> 環境変数を編集で検索 -> 開いて編集
    # 絶対に公開してはいけない
    cookie_value = os.getenv("ATCODER_COOKIE")

    # ページにアクセス
    try:
        user, soup = access(url, cookie_value)
        print(format_text("アクセス成功", fg=SUCCESS_COLOR))
        print(f"{user}\n")
    except Exception as e:
        print(format_text(f"アクセス失敗\n{e}", fg=ERROR_COLOR))
        return
    
    # 問題文やサンプルを取得
    try:
        time_limit_s = get_time_limit(soup)
        input_samples = get_input_samples(soup)
        output_samples = get_output_samples(soup)
        problem_statement = get_problem_statement(soup)
    except Exception as e:
        print(format_text(e, fg=ERROR_COLOR))
        return
    
    # テスト
    src = "./test/atcoder.py"
    test(src, time_limit_s, input_samples, output_samples)

    # 提出前チェック
    check_all(problem_statement)


if __name__ == "__main__":
    main()