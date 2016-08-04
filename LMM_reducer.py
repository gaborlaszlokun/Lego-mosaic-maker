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



# TODO: függvény, ami beolvassa a már legenerált képfájlt és elkészíti kezdetben az 1x1-es leképezését alkatrészekre
def reduce_partlist(img, plate_wid, plate_height):
    img = Image.open(img)
    print img.size[0], img.size[1]
    num_wid = img.size[0] / plate_wid
    pixels = img.load() # create the pixel map
    cntr = 0
    picture = []
    full = 0
    for j in range(0,img.size[1],plate_height):
        for i in range(0,img.size[0],plate_wid):
            picture.append((pixels[i,j], 1))
            cntr += 1
    for item in range(0,len(picture), num_wid):
        line = picture[item: item + num_wid]
        divs = [12, 10, 8, 6, 4, 3, 2] # Array with common Lego-lenghts
        for div in divs:
            for p in range(len(line) - (div - 1)):
                if len(line) > div:
                    part = line[p:p + div]
                    if len(part) > 0:
                        if part.count(part[0]) == div:
                            None
                            line[p:p + div] = [(line[p][0], div)]
        print line, len(line), item / num_wid
        full += len(line)
        print
    print cntr, "db alkatrész kell"
    print full, "a redukált alkatrészszám"

# Usage
img = "tile_20_me.jpg"
img = "plate_20_me.jpg"
reduce_partlist(img, 30, 12)