import requests
from bs4 import BeautifulSoup

import sys
import os
import time
import subprocess

import pyautogui
import pyperclip

import shutil

import itertools
import re


def login(login_data):
    session = requests.Session()
    LOGIN_URL = "https://atcoder.jp/login"
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input",{"name":"csrf_token"})["value"]
    login_data["csrf_token"] = csrf_token
    login_response = session.post(LOGIN_URL, data=login_data)

    HOME_URL = "https://atcoder.jp/home"
    response = session.get(HOME_URL)
    if login_data["username"] not in response.text:
        print("ログイン失敗")
        exit()
    
    print("ログイン成功")
    return session

def get_current_url():
    """現在開いているページのURLを取得（コピペするので気をつける）"""
    pyautogui.click(x=685, y=80)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    current_url = pyperclip.paste()
    pyautogui.hotkey('alt','tab')
    pyautogui.moveTo(1300,900)
    return current_url


class ConfigGetter:
    """サンプルや実行時間制限などを取得する"""
    def __init__(self, session, url):
        self.session = session
        self.url = url
        self.response = session.get(url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
    
    def get_sample(self):
        """入出力サンプルを取得"""
        #サンプルのpreタグを取得
        div_tags = self.soup.find_all("div",class_="part")
        section_tags = [div.find("section") for div in div_tags]
        pre_tags = [section.find_all("pre",recursive=False) for section in section_tags]
        pre_tags = [pre[0] for pre in pre_tags if len(pre) > 0]

        #preタグのなかから、サンプルのみを取り出す
        samples = [pre_tags[i] for i in range(len(pre_tags)) if not pre_tags[i].find()]
        input_samples = [tag.get_text() for i,tag in enumerate(samples) if i % 2 == 0]
        output_samples = [tag.get_text() for i,tag in enumerate(samples) if i % 2 == 1]
        #ABCだと、なぜか2つ同じサンプルを取得してしまうので、同じサンプルがあったら除外
        sample_count = len(input_samples)
        if input_samples[:sample_count//2] == input_samples[sample_count//2:]:
            input_samples = input_samples[sample_count//2:]
            output_samples = output_samples[sample_count//2:]
        
        return input_samples, output_samples
    
    def get_time_limit(self):
        """実行時間制限を取得"""
        p = self.soup.find_all("p")
        for tag in p:
            if "Time Limit" in tag.get_text():
                text = tag.get_text()
                l = text.index(":")+2
                if "msec" in text:
                    r = text.index("msec")-1
                    time_limit = float(text[l:r]) / 1000
                else:
                    r = text.index("sec")-1
                    time_limit = float(text[l:r])
                return time_limit
        return 2 #見つからなかったら2秒ってことにしとく

class Color:
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    WHITE = "\033[37m"

class SampleTester:
    color = {
        "AC": Color.GREEN,
        "WA": Color.YELLOW,
        "RE": Color.YELLOW,
        "CE": Color.YELLOW,
        "TLE": Color.YELLOW,
        "MLE": Color.YELLOW,
    }

    def __init__(self, input_samples, output_samples, time_limit):
        self.input_samples = input_samples
        self.output_samples = output_samples
        self.time_limit = time_limit
    
    def run(self, input_sample, src):
        """プログラムを実行"""
        start_time = time.perf_counter()
        try:
            process = subprocess.Popen(
                ["python", src],  # 実行する Python スクリプト
                stdin=subprocess.PIPE,     # 標準入力をパイプで渡す
                stdout=subprocess.PIPE,    # 標準出力をパイプで受け取る
                stderr=subprocess.PIPE     # 標準エラーをパイプで受け取る
            )

            # 入力データを渡して実行
            stdout, stderr = process.communicate(input=input_sample.encode(),timeout=self.time_limit+0.2)
        except subprocess.TimeoutExpired:
            stdout, stderr = bytes(), bytes()
            process.kill()
        
        elapsed_time = int((time.perf_counter() - start_time) * 1000)
        return stdout, stderr, elapsed_time
    
    def get_result(self, output, correct, err, elapsed_time):
        """出力やエラーから結果を判定"""
        if err:
            return "RE"
        if elapsed_time > self.time_limit * 1000:
            return "TLE"
        if output.split() == correct.split():
            return "AC"
        return "WA"
    
    def print_result(self, sample_number, result, elapsed_time, output, correct, stderr):
        """結果を出力"""
        terminal_width = shutil.get_terminal_size().columns
        color = self.color[result]

        print(f'{color}入力例{sample_number} - {result} - {elapsed_time}ms{Color.WHITE}')
        print(f'{'output':<{terminal_width//2-1}}{color}|{Color.WHITE} correct')
        print(color + '-'*terminal_width + Color.WHITE)

        for output_i, correct_i in itertools.zip_longest(output, correct, fillvalue=""):
            print(f'{output_i:<{terminal_width//2-1}}{color}|{Color.WHITE} {correct_i}')

        print(stderr.decode(errors='ignore'))
    
    def test_one_case(self, sample_number, input_sample, output_sample, src):
        """1つのサンプルを試す"""
        #プログラムを実行
        stdout, stderr, elapsed_time = self.run(input_sample, src)

        #結果を判定
        output = stdout.decode(errors='ignore')
        correct = output_sample
        result = self.get_result(output, correct, stderr, elapsed_time)

        #結果を出力
        output = re.split(r'[\r\n]+', output)
        correct = re.split(r'[\r\n]+', correct)
        self.print_result(sample_number, result, elapsed_time, output, correct, stderr)

        return result
    
    def test(self, src):
        """サンプルをすべて試す"""
        final_result = []
        for sample_number, (input_sample, output_sample) in enumerate(zip(self.input_samples, self.output_samples),1):
            result = self.test_one_case(sample_number, input_sample, output_sample, src)
            final_result.append(f'{self.color[result]}{result}')
        print(*final_result, end=f'{Color.WHITE}\n')


def main():
    args = sys.argv

    #今は削除済み
    #追加したい場合は、スタート -> 環境変数を編集と検索 -> 追加 -> 変数名はATCODER_USERNAME、変数値は値
    username = os.getenv("ATCODER_USERNAME")
    password = os.getenv("ATCODER_PASSWORD")
    login_data = {"username":username,"password":password}

    #今はログインできない
    #session = login(login_data)
    session = requests.Session()
    url = get_current_url()

    getter = ConfigGetter(session, url)
    input_samples, output_samples = getter.get_sample()
    time_limit = getter.get_time_limit()

    tester = SampleTester(input_samples, output_samples, time_limit)
    src = args[1]
    tester.test(src)

if __name__ == '__main__':
    main()