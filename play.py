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
from score import currentScore, lastScore
from image_processor import process_image

def run(w, browser, game_hwnd):
    def isEnd(processed_image):
        matcher = np.copy(processed_image)
        matcher[20,:] = 0
        if np.array_equal(matcher, end_screen):
            return True
        return False
    
    def sigmoid(y):
        z = 1 / (1 + np.exp(-y))
        return z
    
    end_screen = np.load('end_screen.npy')
    
    while True:
        position = win32gui.GetWindowRect(game_hwnd)
        # Take screenshot and process the image
        raw = ImageGrab.grab(position)
        raw = np.array(raw)
        processed_image = process_image(raw)
        
        if isEnd(processed_image):
            break
        
        dim = (418, 418)
        display = cv2.resize(processed_image, dim, interpolation=cv2.INTER_NEAREST)
        
        cv2.imshow("Processed Image", display)
        
        score = currentScore(browser)
        if score != None:
            #print(score)
            pass
        
        x = np.reshape(processed_image, (1, 2500))
        y = sigmoid(x @ w)
        
        # Simulate keyboard input
        if y[0,0] < 0.5:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_UP)
        else:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_UP)
        if y[0,1] >= 0.5 and y[0,2] >= 0.5:
            if y[0,1] > y[0,2]:
                win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT)
            else:
                win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT)
        elif y[0,1] >= 0.5:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT)
        elif y[0,2] >= 0.5:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT)
        if y[0,1] < 0.5:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT)
        if y[0,2] < 0.5:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_LEFT)
        
        cv2.waitKey(25)
    
    cv2.destroyAllWindows()
    return lastScore(browser)