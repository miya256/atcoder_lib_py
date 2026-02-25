from requests import Session
from bs4 import BeautifulSoup, Tag

from terminal_formatter import format_text, print_error, Style


class AtcoderUser:
    COLOR_CODE = {
        "user-gray": "#808080",
        "user-brown": "#8B4513",
        "user-green": "#008000",
        "user-cyan": "#00FFFF",
        "user-blue": "#0000FF",
        "user-yellow": "#FFD700",
        "user-orange": "#FF8C00",
        "user-red": "#FF0000",
    }

    def __init__(self, name: str, rate: str | None, color: str | None) -> None:
        self.name = name
        self.rate = rate
        self.color = AtcoderUser.COLOR_CODE[color] if color in AtcoderUser.COLOR_CODE else "#ffffff"
    
    def __repr__(self):
        name = format_text(self.name, fg=self.color, styles=[Style.Bold])
        rate = format_text(self.rate, fg=self.color)
        return f"{name} {rate}"


def get_user_color(soup: BeautifulSoup) -> str | None:
    username_a = soup.find("a", class_="username")
    if not isinstance(username_a, Tag):
        print_error("ユーザの色を取得できませんでした")
        return None
    
    username_span = username_a.find("span")
    if not isinstance(username_span, Tag):
        print_error("ユーザの色を取得できませんでした")
        return None
    
    user_color = username_span["class"][0]
    return user_color


def get_user_rating(soup: BeautifulSoup) -> str | None:
    table_tag = soup.find("table", class_="dl-table mt-2")
    if not isinstance(table_tag, Tag):
        return None

    rating_th = soup.find("th", string="Rating")
    if not isinstance(rating_th, Tag):
        return None
    
    rating_tr = rating_th.find_parent("tr")
    if not isinstance(rating_tr, Tag):
        return None

    rating_span = rating_tr.find("span")
    if not isinstance(rating_span, Tag):
        return None
    
    rating = rating_span.text
    return rating

def get_user(session: Session, username: str) -> AtcoderUser:
    response = session.get(f"https://atcoder.jp/users/{username}")
    soup = BeautifulSoup(response.text, "html.parser")
    user_color = get_user_color(soup)
    user_rating = get_user_rating(soup)
    return AtcoderUser(username, user_rating, user_color)