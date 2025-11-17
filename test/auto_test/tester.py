import time
import re
import subprocess
import shutil
import itertools

from terminal_formatter import format_text, Style, ERROR_COLOR


RESULT_COLOR = {
    "AC": "#77ff00",
    "WA": "#ffff00",
    "RE": "#ffff00",
    "CE": "#ffff00",
    "TLE": "#ffff00",
    "MLE": "#ffff00",
}


def judge(
    output_sample: str,
    output: str,
    error: str,
    time_limit_s: float,
    elapsed_time: float
) -> str:
    if error:
        return "RE"
    if elapsed_time > time_limit_s:
        return "TLE"
    if output_sample.split() != output.split():
        return "WA"
    return "AC"


def test_one(
    src: str,
    time_limit_s: float,
    input_sample: str,
    output_sample: str
) -> tuple[str, str, str, float]:
    start_s = time.perf_counter()
    try:
        process = subprocess.Popen(
            ["python", src],           # 実行する Python スクリプト
            stdin=subprocess.PIPE,     # 標準入力をパイプで渡す
            stdout=subprocess.PIPE,    # 標準出力をパイプで受け取る
            stderr=subprocess.PIPE     # 標準エラーをパイプで受け取る
        )

        # 入力データを渡して実行
        stdout, stderr = process.communicate(input=input_sample.encode(), timeout=time_limit_s)
    except subprocess.TimeoutExpired:
        stdout, stderr = bytes(), bytes()
        process.kill()

    output = stdout.decode(errors='ignore')
    error = stderr.decode(errors='ignore')
    elapsed_time = time.perf_counter() - start_s
    
    result = judge(
        output_sample,
        output,
        error,
        time_limit_s,
        elapsed_time
    )
    return result, output, error, elapsed_time


def print_result(
    sample_number: int,
    result: str,
    elapsed_time: float,
    correct: str,
    output: str,
    error: str
) -> None:
    terminal_width = shutil.get_terminal_size().columns
    terminal_center = terminal_width//2-1
    color = RESULT_COLOR[result]
    elapsed_time_ms = int(elapsed_time * 1000)

    output_list = re.split(r'[\r\n]+', output)
    correct_list = re.split(r'[\r\n]+', correct)

    print(format_text(
        f"Sample {sample_number} - {result} - {elapsed_time_ms}ms",
        fg=color,
        styles=[Style.Bold]
    ))
    print(f'{'output':<{terminal_center}}{format_text("|", fg=color)} correct')
    print(format_text('-'*terminal_width, fg=color))
    for output_i, correct_i in itertools.zip_longest(output_list, correct_list, fillvalue=""):
        print(f'{output_i:<{terminal_center}}{format_text("|", fg=color)} {correct_i}')
    print(format_text(error, fg=ERROR_COLOR))


def test(
    src: str,
    time_limit_s: float,
    input_samples: list[str],
    output_samples: list[str]
) -> None:
    result_list: list[str] = []
    for i, (input_sample, output_sample) in enumerate(zip(input_samples, output_samples), 1):
        result, output, error, elapsed_time = test_one(src, time_limit_s, input_sample, output_sample)
        print_result(i, result, elapsed_time, output_sample, output, error)
        result_list.append(format_text(result, fg=RESULT_COLOR[result], styles=[Style.Bold]))
    print(*result_list)