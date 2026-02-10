from requests import Session
from bs4 import BeautifulSoup

from user import get_user, AtcoderUser


def check_login(session: Session) -> AtcoderUser:
    #設定ページで確認
    response = session.get("https://atcoder.jp/settings")
    if response.status_code != 200:
        raise Exception(f"ページを取得できませんでした (status={response.status_code})")
    
    #ログインページにリダイレクトされたらログインできてない
    if "https://atcoder.jp/login" in response.url:
        raise Exception("ログインされていませんでした")
    
    soup = BeautifulSoup(response.text, "html.parser")
    icon = soup.find("span", class_="glyphicon glyphicon-cog")
    a = icon.find_parent("a")
    username = a.text.strip()

    user = get_user(session, username)
    return user


def access(url: str, cookie_value: str) -> tuple[AtcoderUser, str]:
    session = Session()
    session.cookies.set("REVEL_SESSION", cookie_value)

    try:
        user: AtcoderUser = check_login(session)
    except:
        raise
    
    response = session.get(url)
    return user, response.text