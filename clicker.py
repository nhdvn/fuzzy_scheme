

import time
import pyautogui


def clicker():
    x = 2670
    y = 500

    for _ in range(6):
        pyautogui.click(x, y)
        x += 370

    x = 2670
    y = 1200

    for _ in range(6):
        pyautogui.click(x, y)
        x += 370


def main():
    delay = 60 * 20

    while True:
        clicker()
        time.sleep(delay)


def check():
    print(pyautogui.position())


main()