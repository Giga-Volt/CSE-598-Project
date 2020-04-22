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
import win32com.client
import time

def process_image(raw):
    processed_image = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)
    (height, width) = processed_image.shape
    processed_image = processed_image[111:height-8, 8:width-8]
    (height, width) = processed_image.shape
    if height < width:
        difference = width - height
        reduction = int(difference / 2)
        processed_image = processed_image[:,reduction:width-reduction]
    elif width < height:
        difference = width - height
        reduction = int(difference / 2)
        processed_image = processed_image[reduction:height-reduction,:]
    dim = (50, 50)
    processed_image = cv2.resize(processed_image, dim, interpolation=cv2.INTER_LANCZOS4)
    return processed_image

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

# Set foreground
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')
win32gui.SetForegroundWindow(game_hwnd)
while True:
    position = win32gui.GetWindowRect(game_hwnd)
    # Take screenshot and process the image
    raw = ImageGrab.grab(position)
    raw = np.array(raw)
    processed_image = process_image(raw)
    
    cv2.imshow("Processed Image", processed_image)
    
    # Simulate keyboard input
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_UP)
    time.sleep(0.1)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_UP)
    
    key = cv2.waitKey(25)
    if key == 27:
        break

cv2.destroyAllWindows()