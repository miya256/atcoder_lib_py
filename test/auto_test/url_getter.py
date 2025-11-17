import pygetwindow as gw
import pyautogui
import pyperclip


BROWSER = "Edge"
EDITOR = "Visual Studio Code"


def get_current_url() -> str:
    windows = gw.getAllWindows()

    for window in windows:
        if BROWSER in window.title:
            browser_window = window
        if EDITOR in window.title:
            editor_window = window

    browser_window.activate()
    pyautogui.hotkey('ctrl', 'l') # URLの欄にカーソル
    pyautogui.hotkey('ctrl', 'c') # コピー
    editor_window.activate()

    url = pyperclip.paste()
    return url