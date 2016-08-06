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
    colorList.append((88,42,18)) # REDDISH BROWN
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
                      
    reduce_partlist(filename, img, plate_wid, plate_height, tile_plate)
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

# Függvény, ami beolvassa a már legenerált képfájlt és elkészíti a redukált alkatrészlistát / MlCad fájlt
def reduce_partlist(filename, img, plate_wid, plate_height, tile_plate):
    if tile_plate == False:
        inner = " 0 1 0 0 0 1 0 0 0 1 "
        y_step = 8
    elif tile_plate == True:
        inner = " 0 1 0 0 0 0 -1 0 1 0 "
        y_step = 20     
    
    num_wid = img.size[0] / plate_wid
    pixels = img.load() # create the pixel map
    cntr = 0
    picture = []
    
    parts = [(1, "3024.dat"),
             (2, "3023.dat"),
             (3, "3623.dat"),
             (4, "3710.dat"),
             (6, "3666.dat"),
             (8, "3460.dat"),
             (10, "4477.dat"),
              (12, "60479.dat")]    
    
    colors = [  
    ((9,19,29), 0), # BLACK
    ((0,85,191), 1), # BLUE
    ((35,120,65), 2), # GREEN
    ((201,26,9), 4), # RED
    ((242,205,55), 14), # YELLOW
    ((255,255,255), 15), # WHITE
    ((228,205,158), 19), # TAN
    ((187,233,11), 27), # LIME
    ((149,138,115), 28), # DARK TAN
    ((172,120,186), 30), # MEDIUM LAVENDER
     ((88,42,18), 70), # REDDISH BROWN
    ((160,165,169), 71),# LIGHT BLUISH GRAY
    ((108,110,104), 72), # DARK BLUISH GRAY
    ((90,147,219), 73), # MEDIUM BLUE
    ((24,70,50), 288), # DARK GREEN
    ((170,127,46), 297), # PEARL GOLD
    ((114,14,15), 320), # DARK RED
    ((155,154,90), 326), # OLIVE GREEN
    ((160,188,172), 378), # SAND GREEN
#    ((228,173,200), 29) # BRIGHT PINK
    ]
    ldr_name = filename.replace(".jpg",".ldr")
    mlcad = '0 Untitled\n0 Name: ' + ldr_name + '\n0 Author: LDraw\n0 Unofficial Model\n0 ROTATION CENTER 0 0 0 1 "Custom" \n0 ROTATION CONFIG 0 0\n'   
    
    full = 0
    y = 0
    for j in range(0,img.size[1],plate_height):
        for i in range(0,img.size[0],plate_wid):
            picture.append((pixels[i,j], 1))
            cntr += 1
    for item in range(0,len(picture), num_wid):
        line = picture[item: item + num_wid]
#        divs = [12, 10, 8, 6, 4, 3, 2] # Array with common Lego-lenghts
        # TODO: kiszervezni fájlba!
        # Original color/ part pairs
        divs = [(12, (0, 4, 14, 15, 19, 70, 71, 72)),
                (10, (0, 1, 2, 4, 14, 15, 19, 70, 71, 72)),
                (8, (0, 1, 2, 4, 14, 15, 19, 27, 30, 70, 71, 72)),
                (6, (0, 1, 2, 4, 14, 15, 19, 27, 28, 30, 70, 71, 72, 73, 288, 320)),
                (4, (0, 1, 2, 4, 14, 15, 19, 27, 28, 30, 70, 71, 72, 73, 288, 320, 378)),
                (3, (0, 1, 2, 4, 14, 15, 19, 27, 28, 70, 71, 72, 73, 288, 320, 378)),
                (2, (0, 1, 2, 4, 14, 15, 19, 27, 28, 30, 70, 71, 72, 73, 288, 320, 326, 378))] # Array with common Lego-lenghts

        # Itt cseréli az RGB értékeket MlCad színkódokra
        for part in range(len(line)):
            for color in range(len(colors)):
                if line[part][0] == colors[color][0]:
                    line[part] = (colors[color][1], line[part][1])
        
        for div in divs:
            color = div[1]
            div = div[0]
            for p in range(len(line) - (div - 1)):
                if len(line) > div:
                    part = line[p:p + div]
                    if len(part) > 0:
                        if part.count(part[0]) == div and part[0][1] == 1:
                            if part[0][0] in color:
                                line[p:p + div] = [(line[p][0], div)]
        print len(line), item / num_wid
        
        for part in range(len(line)):
            # Itt cseréli ki a hosszakat érvényes Lego elemkódokra
            for partname in range(len(parts)):
                if line[part][1] == parts[partname][0]:
                    line[part] = (line[part][0], line[part][1], parts[partname][1])
            # Itt cseréli az RGB értékeket MlCad színkódokra
#            for color in range(len(colors)):
#                if line[part][0] == colors[color][0]:
#                    line[part] = (colors[color][1], line[part][1], line[part][2])
                    
            print line[part]
        
        # TODO: Itt történik meg a tényleges ldr generálása
        x = 0        
        for part in range(len(line)):
            color = str(line[part][0])
            x += line[part][1] * 10
            partcode = line[part][2]
            mlcad_line = "1 " + color + " " + str(x) + " " + str(y) + inner + partcode + "\n"
            mlcad += mlcad_line
            x += line[part][1] * 10
            
        y += y_step   
           
        print
        full += len(line)
    print img.size[0], "x", img.size[1]
    print cntr, "db alkatrész kell"
    print full, "a redukált alkatrészszám"
    mlcad += "0"
    text = open(ldr_name, "w")
    text.write(mlcad)
    text.close()
