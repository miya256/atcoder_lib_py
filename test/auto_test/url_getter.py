import time

import pygetwindow as gw
import pyautogui
import pyperclip


def get_current_url(browser: str, editor: str) -> str:
    windows = gw.getAllWindows()

    browser_window = None
    editor_window = None
    for window in windows:
        if browser in window.title:
            browser_window = window
        if editor in window.title:
            editor_window = window
    
    if browser_window is None:
        raise Exception("ブラウザが見つかりませんでした")
    if editor is None:
        raise Exception("エディタが見つかりませんでした")

    browser_window.activate()
    pyautogui.hotkey('alt', 'd') # URLの欄にカーソル
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c') # コピー
    editor_window.activate()

    url = pyperclip.paste()
    return url