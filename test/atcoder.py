import requests
from bs4 import BeautifulSoup

#atcoderにアクセス -> 開発者ツール -> Aplication -> REVEL_SESSIONの値をコピぺ
#絶対に公開してはいけない
cookie_value = ""

session = requests.Session()
session.cookies.set("REVEL_SESSION", cookie_value)

# ログイン済みページにアクセス
url = "https://atcoder.jp/settings"
resp = session.get(url)
print(resp.url)
# 正常にアクセスできたか確認
if resp.status_code != 200:
    raise Exception(f"アクセス失敗: {resp.status_code}")

# BeautifulSoup で解析
soup = BeautifulSoup(resp.text, "html.parser")
div = soup.find("div", id="main-div")
div = div.find("div", id="main-container")
div = div.find("div", class_="form-group")
print(div)
# ユーザー名を取得
username_elem = soup.select_one("span.navbar-username")  # class 名はページ確認
if username_elem:
    print("ログイン済みユーザー:", username_elem.text.strip())
else:
    print("ユーザー名を取得できません。ログインしているか確認してください。")