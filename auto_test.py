import requests
from bs4 import BeautifulSoup

import os
import time
import subprocess

import pyautogui
import pyperclip

import shutil

import itertools

#手動で変える変数
class Const:
    login_required = False #ログインが必要か。開催中のコンテストの場合はTrue
    has_time_limit = True #実行時間制限を設けるか


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

def get_sample(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    #入出力例の取得
    pre = soup.find_all("pre")
    samples = [pre[i] for i in range(len(pre)) if not pre[i].find()]
    input_samples = [tag.get_text() for i,tag in enumerate(samples) if i % 2 == 0]
    output_samples = [tag.get_text() for i,tag in enumerate(samples) if i % 2 == 1]

    #ABCだと、なぜか2つ同じサンプルを取得してしまうので、同じサンプルがあったら除外
    sample_count = len(input_samples)
    if input_samples[:sample_count//2] == input_samples[sample_count//2:]:
        input_samples = input_samples[sample_count//2:]
        output_samples = output_samples[sample_count//2:]

    #実行時間制限の取得
    if Const.has_time_limit:
        p = soup.find_all("p")
        for tag in p:
            if "Time Limit" in tag.get_text():
                text = tag.get_text()
                l = text.index(":")+1
                r = text.index("sec")
                time_limit = float(text[l:r])
                break
    else:
        time_limit = 60 #実行時間制限を設けない場合は60秒待つ
    
    return time_limit, input_samples, output_samples

def test(sample_num, time_limit, input_sample, output_sample):
    start_time = time.perf_counter()
    try:
        process = subprocess.Popen(
            ["python", "atcoder.py"],  # 実行する Python スクリプト
            stdin=subprocess.PIPE,     # 標準入力をパイプで渡す
            stdout=subprocess.PIPE,    # 標準出力をパイプで受け取る
            stderr=subprocess.PIPE     # 標準エラーをパイプで受け取る
        )

        # 入力データを渡して実行
        stdout, stderr = process.communicate(input=input_sample.encode(),timeout=time_limit+0.2)
    except subprocess.TimeoutExpired:
        stdout, stderr = bytes(), bytes()
        process.kill()

    # 結果を表示
    output = stdout.decode(errors='ignore').split()
    correct = output_sample.split()
    elapsed_time = int((time.perf_counter() - start_time) * 1000)
    if elapsed_time > time_limit * 1000:
        result, color = "TLE", "\033[33m"
    elif output == correct:
        result, color = "AC", "\033[32m"
    elif stderr:
        result, color = "RE", "\033[33m"
    else:
        result, color = "WA", "\033[33m"
    
    terminal_width = shutil.get_terminal_size().columns
    print(f'{color}入力例{sample_num} - {result} - {elapsed_time}ms\033[37m')
    print(f'{'output':<{terminal_width//2-1}}{color}|\033[37m correct')
    print(color + '-'*terminal_width + '\033[37m')
    for output_i, correct_i in itertools.zip_longest(output, correct,fillvalue=""):
        print(f'{output_i:<{terminal_width//2-1}}{color}|\033[37m {correct_i}')
    print(stderr.decode(errors='ignore'))

    return result, color

def get_current_url():
    pyautogui.click(x=685, y=80)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    current_url = pyperclip.paste()
    pyautogui.hotkey('alt','tab')
    pyautogui.moveTo(1300,900)
    return current_url


def main():
    username = os.getenv("ATCODER_USERNAME")
    password = os.getenv("ATCODER_PASSWORD")
    login_data = {"username":username,"password":password}

    #ログインする必要があるならログイン
    session = login(login_data) if Const.login_required else requests.Session()

    url = get_current_url()
    time_limit, input_samples, output_samples = get_sample(session,url)

    all_result = []
    for i, (input_sample, output_sample) in enumerate(zip(input_samples,output_samples),1):
        result,color = test(i, time_limit, input_sample, output_sample)
        all_result.append(f'{color}{result}\033[37m')
    print(*all_result)


if __name__ == '__main__':
    main()
