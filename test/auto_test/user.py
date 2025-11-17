from requests import Session
from bs4 import BeautifulSoup

from terminal_formatter import format_text, Style

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

    def __init__(self, name: str, rate: int, color: str) -> None:
        self.name = name
        self.rate = rate
        self.color = color
    
    def __repr__(self):
        name = format_text(self.name, fg=AtcoderUser.COLOR_CODE[self.color], styles=[Style.Bold])
        rate = format_text(self.rate, fg=AtcoderUser.COLOR_CODE[self.color])
        return f"{name} {rate}"


def get_user(session: Session, username: str) -> AtcoderUser:
    response = session.get(f"https://atcoder.jp/users/{username}")
    soup = BeautifulSoup(response.text, "html.parser")
    usercolor = soup.find("a", class_="username").find("span")["class"][0]
    userrate = soup.find("table", class_="dl-table mt-2").find("span", class_=usercolor).text
    return AtcoderUser(username, int(userrate), usercolor)