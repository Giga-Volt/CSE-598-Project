# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:20:26 2020

@author: Gaurang Vichare
"""

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