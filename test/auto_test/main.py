import os

from access import access
from terminal_formatter import format_text, SUCCESS_COLOR, ERROR_COLOR
from problem_info import get_time_limit, get_input_samples, get_output_samples
from tester import test


def main():
    url = "https://atcoder.jp/contests/abc432/tasks/abc432_e"

    #atcoderにアクセス -> 開発者ツール -> Aplication -> REVEL_SESSION の値をコピぺ
    #スタート -> 環境変数を編集で検索 -> 開いて編集
    #絶対に公開してはいけない
    cookie_value = os.getenv("ATCODER_COOKIE")
    try:
        user, soup = access(url, cookie_value)
        print(format_text("アクセス成功", fg=SUCCESS_COLOR))
        print(f"{user}\n")
    except Exception as e:
        print(format_text(f"アクセス失敗\n{e}", fg=ERROR_COLOR))
        return
    
    try:
        time_limit_s = get_time_limit(soup)
        input_samples = get_input_samples(soup)
        output_samples = get_output_samples(soup)
    except Exception as e:
        print(format_text(e, fg=ERROR_COLOR))
    
    src = "./test/atcoder.py"
    test(src, time_limit_s, input_samples, output_samples)


if __name__ == "__main__":
    main()