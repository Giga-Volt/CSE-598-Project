# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 12:26:16 2020

@author: Gaurang Vichare
"""

from selenium import webdriver
import time

driver_path = 'C:\\Users/gvich/Downloads/chromedriver_win32/chromedriver'

browser = webdriver.Chrome(executable_path=driver_path)
browser.get('http://slither.io/')

while True:
    html = browser.page_source
    start = 'Your length: </span><span style="opacity: .8; font-weight: bold;">'
    end = '</span></span><br><span style="opacity: .3;">'
    index1 = html.find(start)
    index2 = html.find(end)
    if index1 == -1 or index2 == -1:
        continue
    n = len(start)
    score = int(html[index1+n:index2])
    print(score)
    time.sleep(0.1)