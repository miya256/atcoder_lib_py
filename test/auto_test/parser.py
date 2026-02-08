import re
from typing import Optional

from bs4 import BeautifulSoup


class ProblemSpec:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, "html.parser")

        self.time_limit_s: float = self._parse_time_limit()
        self.input_samples: dict[Optional[str]] = self._parse_input_samples()
        self.output_samples: dict[Optional[str]] = self._parse_output_samples()
        self.problem_statement: Optional[str] = self._parse_problem_statement()
    
    def _parse_time_limit(self) -> float:
        for tag in self.soup.find_all("p"):
            if "Time Limit" not in tag.text:
                continue
            if match := re.search(r"Time Limit:\s*([\d.]+)\s*(sec|msec).*", tag.text):
                value = float(match.group(1))
                unit = match.group(2)
                if unit == "msec":
                    value /= 1000
                return value
            else:
                # raise Exception(f"実行時間制限が期待した文字列と一致しませんでした: {tag.text!r}")
                return 2.0 # 見つからなかったらとりあえず2秒
        # raise Exception("実行時間制限が見つかりませんでした")
        return 2.0
    
    def _parse_input_samples(self) -> dict[Optional[str]]:
        input_samples = {}
        for tag in self.soup.find_all("h3"):
            if match := re.search(r"入力例 (\d)", tag.text):
                sample_number = int(match.group(1))
                if sample_number in input_samples:
                    # raise Exception(f"入力例番号に重複が見られました: 入力例 {sample_number}")
                    input_samples[sample_number] = None
                    continue
                pre = tag.find_next("pre")
                input_samples[sample_number] = pre.text
        return input_samples
    
    def _parse_output_samples(self) -> dict[Optional[str]]:
        output_samples = {}
        for tag in self.soup.find_all("h3"):
            if match := re.search(r"出力例 (\d)", tag.text):
                sample_number = int(match.group(1))
                if sample_number in output_samples:
                    # raise Exception(f"出力例番号に重複が見られました: 出力例 {sample_number}")
                    output_samples[sample_number] = None
                    continue
                pre = tag.find_next("pre")
                output_samples[sample_number] = pre.text
        return output_samples
    
    def _parse_problem_statement(self) -> Optional[str]:
        section = self.soup.find("section")
        if section is None or "問題文" not in section.find_next("h3"):
            # raise Exception("問題文の取得に失敗しました")
            return None
        return section.text.strip()