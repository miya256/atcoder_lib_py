import pygetwindow as gw
import pyautogui
import pyperclip


def get_current_url(browser: str, editor: str) -> str:
    windows = gw.getAllWindows()

    for window in windows:
        if browser in window.title:
            browser_window = window
        if editor in window.title:
            editor_window = window

    browser_window.activate()
    pyautogui.hotkey('ctrl', 'l') # URLの欄にカーソル
    pyautogui.hotkey('ctrl', 'c') # コピー
    editor_window.activate()

    url = pyperclip.paste()
    return url