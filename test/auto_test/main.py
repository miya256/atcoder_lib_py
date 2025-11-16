import os

from access import access
from terminal_format import format_text, Style

def main():
    url = "https://atcoder.jp/contests/abc432"

    #atcoderにアクセス -> 開発者ツール -> Aplication -> REVEL_SESSION の値をコピぺ
    #スタート -> 環境変数を編集で検索 -> 開いて編集
    #絶対に公開してはいけない
    cookie_value = os.getenv("ATCODER_COOKIE")
    try:
        user, soup = access(url, cookie_value)
        print(format_text("アクセス成功", fg="#00ff00"))
        print(user)
    except Exception as e:
        print(format_text(f"アクセス失敗\n{e}", fg="#dd0000"))
        return


if __name__ == "__main__":
    main()