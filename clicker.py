

import time
import pyautogui

def clicker():
    x = 2700
    y = 550

    for _ in range(4):
        pyautogui.click(x, y)
        x += 500

    x = 2700
    y = 1200

    for _ in range(4):
        pyautogui.click(x, y)
        x += 450

delay = 60 * 20

while True:
    clicker()
    time.sleep(delay)