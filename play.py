# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 21:28:54 2020

@author: Gaurang Vichare
"""

import cv2
import numpy as np
from PIL import ImageGrab
import win32gui
import win32api
import win32con
import time

# Detect the game window
windows_list = []
toplist = []
def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))
win32gui.EnumWindows(enum_win, toplist)

# Game handle
game_hwnd = 0
for (hwnd, win_text) in windows_list:
    if "slither.io" in win_text:
        game_hwnd = hwnd

while True:
    position = win32gui.GetWindowRect(game_hwnd)
    # Take screenshot
    screenshot = ImageGrab.grab(position)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    cv2.imshow("Screen", screenshot)
    
    # Simulate keyboard input
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_UP)
    time.sleep(0.5)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_UP)
    
    key = cv2.waitKey(25)
    if key == 27:
        break

cv2.destroyAllWindows()