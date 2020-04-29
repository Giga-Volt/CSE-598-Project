# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 21:35:35 2020

@author: Gaurang Vichare
"""

import cv2

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
    height = width = 13
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

def get_matcher(raw):
    matcher = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)
    (height, width) = matcher.shape
    matcher = matcher[124:height-8, 8:width-8]
    (height, width) = matcher.shape
    if height < width:
        difference = width - height
        reduction = int(difference / 2)
        matcher = matcher[:,reduction:width-reduction]
    elif width < height:
        difference = width - height
        reduction = int(difference / 2)
        matcher = matcher[reduction:height-reduction,:]
    height = width = 50
    dim = (height, width)
    matcher = cv2.resize(matcher, dim, interpolation=cv2.INTER_LANCZOS4)
    for i in range(height):
        for j in range(width):
            value = matcher[i][j]
            if value <= 63:
                matcher[i][j] = 0
            elif value <= 127:
                matcher[i][j] = 96
            elif value <= 191:
                matcher[i][j] = 160
            else:
                matcher[i][j] = 255
    return matcher