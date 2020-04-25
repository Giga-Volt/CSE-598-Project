# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:49:54 2020

@author: Gaurang Vichare
"""

from selenium import webdriver
import win32gui
import win32com.client
import win32api
import win32con
import time

def launchGame():
    browser = webdriver.Chrome()
    browser.get('http://slither.io/')
    
    browser.set_window_size(900, 550)
    
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
    
    input('Enter a name and change the snake to white. Then give an input:')
    time.sleep(10)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN)
    
    #time.sleep(1)
    
    return browser, game_hwnd