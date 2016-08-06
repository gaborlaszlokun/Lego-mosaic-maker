# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 16:32:36 2016

@author: ASUS
"""

#import PIL
from PIL import Image
#import math
#import numpy as np
#import operator 

# Függvény, ami beolvassa a már legenerált képfájlt és elkészíti a redukált alkatrészlistát / MlCad fájlt
def reduce_partlist(image, plate_wid, plate_height, tile_plate):
    if tile_plate == False:
        inner = " 0 1 0 0 0 1 0 0 0 1 "
        y_step = 8
    elif tile_plate == True:
        inner = " 0 1 0 0 0 0 -1 0 1 0 "
        y_step = 20   
    
    img = Image.open(image)
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
    ldr_name = str(image).replace(".jpg",".ldr")
    mlcad = '0 Untitled\n0 Name: ' + ldr_name + '\n0 Author: LDraw\n0 Unofficial Model\n0 ROTATION CENTER 0 0 0 1 "Custom" \n0 ROTATION CONFIG 0 0\n'   
    
    full = 0
    y = 0
    for j in range(0,img.size[1],plate_height):
        for i in range(0,img.size[0],plate_wid):
            picture.append((pixels[i,j], 1))
            cntr += 1
    for item in range(0,len(picture), num_wid):
        line = picture[item: item + num_wid]
        # TODO: refactor me pls
        divs = []
        cols = open("original.col", "r")
        alldiv = cols.read()
        cols.close()
        alldiv = alldiv.split("\n")
        for lin in alldiv:
            lens = ()
            for  length in lin.split("  ")[1].split(" "):
                lens += (int(length),)
            divs.append((int(lin.split("  ")[0]), (lens)))
            
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
                    
            print line[part]
        
        #  Itt történik meg a tényleges ldr generálása
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
#    print mlcad
    text = open(ldr_name, "w")
    text.write(mlcad)
    text.close()

# Usage
#img = "tile_20_me.jpg"
img = "tile_20_me.jpg"
#reduce_partlist(img, 30, 12)
reduce_partlist(img, 30, 30, True)