from pathlib import Path
import time
import re
import subprocess
import shutil
import difflib
from itertools import zip_longest

from terminal_formatter import format_text, Style, ERROR_COLOR
from parser import ProblemSpec


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
    elapsed_time: float,
) -> str:
    if error:
        return "RE"
    if elapsed_time > time_limit_s:
        return "TLE"
    if output_sample.split() != output.split():
        return "WA"
    return "AC"


def test_one(
    src_path: Path, time_limit_s: float, input_sample: str, output_sample: str
) -> tuple[str, str, str, float]:
    start_s = time.perf_counter()
    process = subprocess.Popen(
        ["python", src_path],  # 実行する Python スクリプト
        stdin=subprocess.PIPE,  # 標準入力をパイプで渡す
        stdout=subprocess.PIPE,  # 標準出力をパイプで受け取る
        stderr=subprocess.PIPE,  # 標準エラーをパイプで受け取る
    )
    try:
        # 入力データを渡して実行
        stdout, stderr = process.communicate(input=input_sample.encode(), timeout=time_limit_s)
    except subprocess.TimeoutExpired:
        stdout, stderr = bytes(), bytes()
        process.kill()

    output = stdout.decode(errors="ignore")
    error = stderr.decode(errors="ignore")
    elapsed_time = time.perf_counter() - start_s

    result = judge(output_sample, output, error, time_limit_s, elapsed_time)
    return result, output, error, elapsed_time


def print_result(
    sample_number: int,
    result: str,
    elapsed_time: float,
    correct: str,
    output: str,
    error: str,
) -> None:
    def format_diff(output: str, correct: str) -> tuple[str, str]:
        """差分に色をつける"""
        diff_color = "#00ffff"

        # 色つけてからだと、ターミナルの文字がずれるので、先にpadding
        output = "\n".join([f"{output_i:<{terminal_center}}" for output_i in output.splitlines()])
        correct = "\n".join([f"{correct_i}" for correct_i in correct.splitlines()])

        output_tokens = re.split(r"(\s+)", output) if output else []
        correct_tokens = re.split(r"(\s+)", correct) if correct else []
        sm = difflib.SequenceMatcher(None, output_tokens, correct_tokens)

        new_output = []
        new_correct = []
        for tag, li, ri, lj, rj in sm.get_opcodes():
            for output_token, correct_token in zip_longest(
                output_tokens[li:ri], correct_tokens[lj:rj], fillvalue=""
            ):
                if tag == "equal":
                    new_output.append(output_token)
                    new_correct.append(correct_token)
                elif tag == "replace":
                    new_output.append(format_text(output_token, fg=diff_color))
                    new_correct.append(format_text(correct_token, fg=diff_color))
                elif tag == "delete":
                    new_output.append(format_text(output_token, fg=diff_color))
                elif tag == "insert":
                    new_correct.append(format_text(correct_token, fg=diff_color))

        return "".join(new_output), "".join(new_correct)

    terminal_width = shutil.get_terminal_size().columns
    terminal_center = terminal_width // 2 - 1
    color = RESULT_COLOR[result]
    elapsed_time_ms = int(elapsed_time * 1000)

    output, correct = format_diff(output, correct)

    print(
        format_text(
            f"Sample {sample_number} - {result} - {elapsed_time_ms}ms",
            fg=color,
            styles=[Style.Bold],
        )
    )
    print(f"{'output': <{terminal_center}}{format_text('|', fg=color)} correct")
    print(format_text("-" * terminal_width, fg=color))

    for output_i, correct_i in zip_longest(
        output.splitlines(), correct.splitlines(), fillvalue=" " * terminal_center
    ):
        print(f"{output_i}{format_text('|', fg=color)} {correct_i}")

    print(format_text(error, fg=ERROR_COLOR))


def test(src_path: Path, problem_spec: ProblemSpec) -> None:
    result_list: list[str] = []
    input_samples = problem_spec.input_samples
    output_samples = problem_spec.output_samples
    for i in sorted(set(input_samples.keys()) | set(output_samples.keys())):
        if (
            i not in input_samples
            or i not in output_samples
            or input_samples[i] is None
            or output_samples[i] is None
        ):
            message = (
                format_text(
                    f"Sample {i} - 入出力例の組みが存在しませんでした",
                    fg="#000000",
                    bg="#ffff00",
                    styles=[Style.Bold],
                )
                + "\n"
            )
            result_list.append(format_text("SKIP", fg="#000000", bg="#ffff00", styles=[Style.Bold]))
            print(message)
            continue

        input_sample = input_samples[i]
        output_sample = output_samples[i]
        assert input_sample is not None
        assert output_sample is not None
        result, output, error, elapsed_time = test_one(
            src_path, problem_spec.time_limit_s, input_sample, output_sample
        )
        print_result(i, result, elapsed_time, output_sample, output, error)
        result_list.append(format_text(result, fg=RESULT_COLOR[result], styles=[Style.Bold]))
    print(*result_list)
