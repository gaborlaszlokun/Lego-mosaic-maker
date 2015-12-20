# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:14:17 2015

@author: Eniac II
"""

import PIL
from PIL import Image
from collections import Counter
import math
import operator 

"""
    color codes:
        white: 255,255,255
        black: 5,19,29
        dark b. grey: 108,110,104
        light b. grey: 160,165,169
		etc...
"""

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


"""" Input"""
img = Image.open("me.jpg")

wid = 200 # width in pixels
wpercent = (wid/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
hsize = hsize - (hsize % 2)
img = img.resize((wid,hsize), PIL.Image.ANTIALIAS)
pixels = img.load() # create the pixel map

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)



def getColor(color):    
    dists = []
    for i in colorList:
        
        dists.append((i,euclideanDistance(color, i, 3)))
    dists.sort(key=operator.itemgetter(1))
    return dists[0][0]

for i in range(img.size[0]):
    for j in range(img.size[1]):
            r = pixels[i,j][0] 
            g = pixels[i,j][1] 
            b = pixels[i,j][2]
            color = (r, g, b)
            newcolor = getColor(color)
            pixels[i,j] = newcolor


def plater():
    for i in range(0,img.size[0],5):
        for j in range(0,img.size[1],2):
            colors = []
            for k in range(5):
                for l in range (2):
                    colors.append(pixels[i+k,j+l])
            color_counts = Counter(colors)
            color = color_counts.most_common(1)[0][0]
            for k in range(5):
                for l in range (2):
                    pixels[i+k,j+l] = color

def tiler():
    for i in range(0,img.size[0],5):
        for j in range(0,img.size[1],5):
            colors = []
            for k in range(5):
                for l in range (5):
                    colors.append(pixels[i+k,j+l])
            color_counts = Counter(colors)
            color = color_counts.most_common(1)[0][0]
            for k in range(5):
                for l in range (5):
                    pixels[i+k,j+l] = color

plater() # using only 1x1 plates
#tiler() # using only 1x1 tiles


c = 0
for i in range(0,img.size[0],5):
    for j in range(0,img.size[1],2):
        x, y = int(i/5), int(j/2)
        c += 1

x = wid/5
y = hsize/2
print x, y
print x * y, "darab elem"
 
platelist = [[0 for q in range(x)] for q in range(y)] 
print len(platelist)       
for i in range(0,img.size[0],5):
    for j in range(0,img.size[1],2):
        u = int(i/5)
        v = int(j/2)
        if pixels[i,j][0:3] == (255, 255, 255):
            platelist[v][u] = ('w', 3024)
        elif pixels[i,j][0:3] == (9, 19, 29):
            platelist[v][u] = ('b', 3024)

#img.show() # show result
img.save("me_100.png","PNG")