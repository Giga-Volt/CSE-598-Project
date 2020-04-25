# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 19:48:00 2020

@author: Gaurang Vichare
"""

import win32gui
import win32api
import win32con
import numpy as np
import cv2
from PIL import ImageGrab
import time
from initialize import launchGame

def process_image(raw):
    processed_image = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)
    (height, width) = processed_image.shape
    processed_image = processed_image[124:height-8, 8:width-8]
    (height, width) = processed_image.shape
    if height < width:
        difference = width - height
        reduction = int(difference / 2)
        processed_image = processed_image[:,reduction:width-reduction]
    elif width < height:
        difference = width - height
        reduction = int(difference / 2)
        processed_image = processed_image[reduction:height-reduction,:]
    height = width = 50
    dim = (height, width)
    processed_image = cv2.resize(processed_image, dim, interpolation=cv2.INTER_LANCZOS4)
    for i in range(height):
        for j in range(width):
            value = processed_image[i][j]
            if value <= 63:
                processed_image[i][j] = 0
            elif value <= 127:
                processed_image[i][j] = 96
            elif value <= 191:
                processed_image[i][j] = 160
            else:
                processed_image[i][j] = 255
    return processed_image

def isEnd(processed_image):
    if np.array_equal(processed_image, end_screen):
        return True
    return False

def lastScore(browser):
    html = browser.page_source
    start = 'Your final length was </span><b>'
    end = '</b></div>'
    index1 = html.find(start)
    index2 = html.find(end)
    n = len(start)
    score = int(html[index1+n:index2])
    return score

def currentScore(browser):
    # Get current score
    html = browser.page_source
    start = 'Your length: </span><span style="opacity: .8; font-weight: bold;">'
    end = '</span></span><br><span style="opacity: .3;">'
    index1 = html.find(start)
    index2 = html.find(end)
    if index1 == -1 or index2 == -1:
        return
    n = len(start)
    score = int(html[index1+n:index2])
    return score

end_screen = np.load('end_screen.npy')

browser, game_hwnd = launchGame();

while True:
    position = win32gui.GetWindowRect(game_hwnd)
    # Take screenshot and process the image
    raw = ImageGrab.grab(position)
    raw = np.array(raw)
    processed_image = process_image(raw)
    
    if isEnd(processed_image):
        print('Last Score:', lastScore(browser))
        break
    
    dim = (418, 418)
    display = cv2.resize(processed_image, dim, interpolation=cv2.INTER_NEAREST)
    
    cv2.imshow("Processed Image", display)
    
    score = currentScore(browser)
    if score != None:
        print(score)
    
    # Simulate keyboard input
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_UP)
    time.sleep(0.1)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_UP)
    
    cv2.waitKey(25)

cv2.destroyAllWindows()