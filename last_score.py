# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:20:26 2020

@author: Gaurang Vichare
"""

from selenium import webdriver

driver_path = 'C:\\Users/gvich/Downloads/chromedriver_win32/chromedriver'

browser = webdriver.Chrome(executable_path=driver_path)
browser.get('http://slither.io/')

value = input("Enter anything to record score:\n")

# This will get the initial html - before javascript
html = browser.page_source
start = 'Your final length was </span><b>'
end = '</b></div>'
index1 = html.find(start)
index2 = html.find(end)
n = len(start)
score = int(html[index1+n:index2])
print(score)