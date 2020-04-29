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
import neat
import os
import pickle
from initialize import launchGame
from score import currentScore, lastScore
from image_processor import process_image, get_matcher

def pressUp(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_UP)

def pressRight(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT)

def pressLeft(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT)

def releaseUp(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_UP)

def releaseRight(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT)

def releaseLeft(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_LEFT)

def releaseAll(game_hwnd):
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_UP)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_LEFT)

def main(genomes, config):
    for _, g in genomes:
        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN)
        win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN)
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = evalGenome(net, browser, game_hwnd)

def evalGenome(net, browser, game_hwnd):
    def isEnd(raw):
        matcher = get_matcher(raw)
        matcher[20,:] = 0
        if np.array_equal(matcher, end_screen):
            return True
        return False
    
    def sigmoid(y):
        z = 1 / (1 + np.exp(-y))
        return z
    
    suicide = False
    scores = []
    
    while True:
        position = win32gui.GetWindowRect(game_hwnd)
        # Take screenshot and process the image
        raw = ImageGrab.grab(position)
        raw = np.array(raw)
        processed_image = process_image(raw)
        
        if isEnd(raw):
            break
        
        #dim = (418, 418)
        #display = cv2.resize(processed_image, dim, interpolation=cv2.INTER_NEAREST)
        #cv2.imshow("Processed Image", display)
        
        score = currentScore(browser)
        if score != None:
            #print(score)
            if len(scores) == 300:
                scores = scores[1:300]
            scores.append(score)
            pass
        
        if len(scores) == 300:
            scoresArray = np.array(scores)
            if np.std(scoresArray) < 1:
                suicide = True
        
        if suicide:
            releaseAll(game_hwnd)
        else:
            x = processed_image.flatten()
            x = x - 128
            x = x.tolist()
            
            y = net.activate(x)
            
            # Simulate keyboard input
            if y[0] < 0:
                releaseUp(game_hwnd)
            else:
                pressUp(game_hwnd)
            if y[1] >= 0 and y[2] >= 0:
                if y[1] > y[2]:
                    pressRight(game_hwnd)
                else:
                    pressLeft(game_hwnd)
            elif y[1] >= 0:
                pressRight(game_hwnd)
            elif y[2] >= 0:
                pressLeft(game_hwnd)
            if y[1] < 0:
                releaseRight(game_hwnd)
            if y[2] < 0:
                releaseLeft(game_hwnd)
        
        cv2.waitKey(25)
    
    releaseAll(game_hwnd)
    cv2.destroyAllWindows()
    return lastScore(browser)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main, 1)
    
    filename = 'best'
    outfile = open(filename,'wb')
    pickle.dump(winner, outfile)
    outfile.close()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    end_screen = np.load('end_screen.npy')
    browser, game_hwnd = launchGame();
    run(config_path)