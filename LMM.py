# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 13:00:56 2016

@author: ASUS
"""

import PIL
from PIL import Image
import math
import numpy as np
import operator 

def full_color_list():
    colorList = []
    colorList.append((9,19,29)) # BLACK
    colorList.append((255,255,255)) # WHITE
    colorList.append((108,110,104)) # DARK BLUISH GRAY
    colorList.append((160,165,169)) # LIGHT BLUISH GRAY
    colorList.append((228,205,158)) # TAN
    colorList.append((149,138,115)) # DARK TAN
    colorList.append((0,85,191)) # BLUE
    colorList.append((90,147,219)) # MEDIUM BLUE
    colorList.append((242,205,55)) # YELLOW
    colorList.append((114,14,15)) # DARK RED
    colorList.append((172,120,186)) # MEDIUM LAVENDER
    colorList.append((170,127,46)) # PEARL GOLD
    colorList.append((160,188,172)) # SAND GREEN
    colorList.append((24,70,50)) # DARK GREEN
    colorList.append((35,120,65)) # GREEN
    colorList.append((187,233,11)) # LIME
    colorList.append((155,154,90)) # OLIVE GREEN
    colorList.append((201,26,9)) # RED
    colorList.append((88,42,18)) # REDDIH BROWN
#    colorList.append((228,173,200)) # BRIGHT PINK
    return colorList
    
def bw_color_list():
    colorList = []
    colorList.append((9,19,29)) # BLACK
    colorList.append((255,255,255)) # WHITE
    return colorList

def grayscale_color_list():
    colorList = []
    colorList.append((9,19,29)) # BLACK
    colorList.append((255,255,255)) # WHITE
    colorList.append((108,110,104)) # DARK BLUISH GRAY
    colorList.append((160,165,169)) # LIGHT BLUISH GRAY
    return colorList
    
def generate_mosaic(filename, num_wid, tile_plate):
    img = Image.open(filename)
    x = img.size[0]
    y = img.size[1]
    print x, y
    full_wid = 5 * num_wid
    if x % full_wid > full_wid / 2:
        wid = (x - x % full_wid) + full_wid
    else:
        wid = (x - x % full_wid)
    wpercent = (wid/float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    plate_wid = wid / num_wid
    
    if tile_plate == True:
        plate_height = plate_wid
        filename = "tile_" + str(num_wid) + "_" + filename
    else:
        plate_height = int(plate_wid / 2.5)
        filename = "plate_" + str(num_wid) + "_" + filename
    
    hsize = hsize - (hsize % plate_height)
    img = img.resize((wid,hsize), PIL.Image.ANTIALIAS)
    print img.size[0], img.size[1]
    pixels = img.load() # create the pixel map
    for i in range(0,img.size[0],plate_wid):
        for j in range(0,img.size[1],plate_height):
            reds = []
            greens = []
            blues = []
            for k in range(plate_wid):
                for l in range(plate_height):
                    reds.append(pixels[i+k,j+l][0])
                    greens.append(pixels[i+k,j+l][1])
                    blues.append(pixels[i+k,j+l][2])
            
            r =  int(round(np.mean(reds)))
            g =  int(round(np.mean(greens)))
            b =  int(round(np.mean(blues)))
            color = (r, g, b)
            for k in range(plate_wid):
                for l in range(plate_height):
                    pixels[i+k,j+l] = color
    for i in range(img.size[0]):
        for j in range(img.size[1]):
                r = pixels[i,j][0] 
                g = pixels[i,j][1] 
                b = pixels[i,j][2]
                color = (r, g, b)
                newcolor = getColor(color)
                pixels[i,j] = newcolor
    img.save(filename,"PNG")

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)



def getColor(color):
    colorList = full_color_list()    
    dists = []
    for i in colorList:
                dists.append((i,euclideanDistance(color, i, 3)))
    dists.sort(key=operator.itemgetter(1))
    return dists[0][0]
