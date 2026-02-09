import re
from typing import Optional

from bs4 import BeautifulSoup

from terminal_formatter import format_text, ERROR_COLOR


class ProblemSpec:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, "html.parser")

        self.time_limit_s: float = self._parse_time_limit() # 実行時間制限
        self.memory_limit_mib: int = self._parse_memory_limit() # メモリ制限
        self.output_statement: Optional[str] = self._parse_output_statement() # 出力形式の説明
        self.input_samples: dict[Optional[str]] = self._parse_input_samples() # 入力例
        self.output_samples: dict[Optional[str]] = self._parse_output_samples() # 出力例
        self.problem_statement: Optional[str] = self._parse_problem_statement() # 問題文
        print(self.input_samples)

    def _print_parse_error(self, message) -> None:
        print(format_text(message, fg=ERROR_COLOR))
    
    def _parse_time_limit(self) -> float:
        default_time_limit = 2.0
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
                self._print_parse_error(f"実行時間制限が期待した文字列と一致しませんでした: {tag.text!r}")
                return default_time_limit
        self._print_parse_error("実行時間制限が見つかりませんでした")
        return default_time_limit
    
    def _parse_memory_limit(self) -> int:
        default_memory_limit = 1024
        for tag in self.soup.find_all("p"):
            if "Memory Limit" not in tag.text:
                continue
            if match := re.search(r".*Memory Limit: (\d+) MiB", tag.text):
                value = int(match.group(1))
                return value
            else:
                self._print_parse_error(f"メモリ制限が期待した文字列と一致しませんでした: {tag.text!r}")
                return default_memory_limit
        self._print_parse_error("メモリ制限が見つかりませんでした")
        return default_memory_limit
    
    def _parse_output_statement(self) -> Optional[str]:
        for tag in self.soup.find_all("h3"):
            if tag.text == "出力":
                return tag.find_next().text
        self._print_parse_error("出力の説明文の取得に失敗しました")
        return None
    
    def _parse_input_samples(self) -> dict[Optional[str]]:
        input_samples = {}
        for tag in self.soup.find_all("h3"):
            if match := re.search(r"入力例 (\d)", tag.text):
                sample_number = int(match.group(1))
                if sample_number in input_samples:
                    self._print_parse_error(f"入力例番号に重複が見られました: 入力例 {sample_number}")
                    input_samples[sample_number] = None
                    continue
                pre = tag.find_next("pre")
                input_samples[sample_number] = pre.text.lstrip("\n")
        return input_samples
    
    def _parse_output_samples(self) -> dict[Optional[str]]:
        output_samples = {}
        for tag in self.soup.find_all("h3"):
            if match := re.search(r"出力例 (\d)", tag.text):
                sample_number = int(match.group(1))
                if sample_number in output_samples:
                    self._print_parse_error(f"出力例番号に重複が見られました: 出力例 {sample_number}")
                    output_samples[sample_number] = None
                    continue
                pre = tag.find_next("pre")
                output_samples[sample_number] = pre.text.lstrip("\n")
        return output_samples
    
    def _parse_problem_statement(self) -> Optional[str]:
        section = self.soup.find("section")
        if section is None or "問題文" not in section.find_next("h3"):
            self._print_parse_error("問題文の取得に失敗しました")
            return None
        return section.text.strip()