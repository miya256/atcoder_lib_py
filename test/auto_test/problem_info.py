import re

from bs4 import BeautifulSoup


def get_time_limit(soup: BeautifulSoup) -> float:
    for tag in soup.find_all("p"):
        if "Time Limit" not in tag.text:
            continue
        if match := re.search(r"Time Limit:\s*([\d.]+)\s*(sec|msec).*", tag.text):
            value = float(match.group(1))
            unit = match.group(2)
            if unit == "msec":
                value /= 1000
            return value
        else:
            raise Exception(f"実行時間制限が期待した文字列と一致しませんでした: {tag.text!r}")
    raise Exception("実行時間制限が見つかりませんでした")

#preタグだけじゃわからないので、
# 前の入力例1という文字とかから頑張って判定する
def get_input_samples(soup: BeautifulSoup) -> list[str]:
    input_samples = []
    for tag in soup.find_all("h3"):
        if match := re.search(r"入力例 (\d)", tag.text):
            sample_number = int(match.group(1))
            expected = len(input_samples) + 1
            if sample_number != expected:
                raise Exception(f"入力例の番号が異なります: expected={expected}, actual={sample_number}")
            pre = tag.find_next("pre")
            input_samples.append(pre.text)
    return input_samples


def get_output_samples(soup: BeautifulSoup) -> list[str]:
    output_samples = []
    for tag in soup.find_all("h3"):
        if match := re.search(r"出力例 (\d)", tag.text):
            sample_number = int(match.group(1))
            expected = len(output_samples) + 1
            if sample_number != expected:
                raise Exception(f"出力例の番号が異なります: expected={expected}, actual={sample_number}")
            pre = tag.find_next("pre")
            output_samples.append(pre.text)
    return output_samples