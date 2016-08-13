# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 13:00:56 2016

@author: ASUS
"""

import PIL
from PIL import Image
import math
import numpy as np
import pandas as pd
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
#    colorList = grayscale_color_list()
#    colorList = bw_color_list()
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
    
    parts = pd.read_csv("plates_colors.csv")
    
    # TODO: kiszervezni fájlba!
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
    
    y = 0
    
    # MlCad DataFrame inicializálása
    columns = ['color', 'x', 'y', 'inner', 'partcode']
    mlcad_df = pd.DataFrame(columns=columns)
    index = 0
    
    # Képból 2D-s tömb generálása
    for j in range(0,img.size[1],plate_height):
        for i in range(0,img.size[0],plate_wid):
            picture.append((pixels[i,j], 1))
            cntr += 1
    
    # Főciklus, képtömb feldolgozása sorról sorra       
    for item in range(0,len(picture), num_wid):
        # Select a num_wid-long line from the generated picture
        line = picture[item: item + num_wid]
        
        # Itt cseréli az RGB értékeket MlCad színkódokra
        for part in range(len(line)):
            for color in range(len(colors)):
                if line[part][0] == colors[color][0]:
                    line[part] = (colors[color][1], line[part][1])
        
        # Itt cseréli sorfolytonosan az elemeket nagyobbakra, ha az adott színű elem létezik
        for k in range(len(parts)):
            color = parts.iat[-k,3].split(";")
            div = parts.iat[-k,0]
            for p in range(len(line) - (div - 1)):
                if len(line) > div:
                    part = line[p:p + div]
                    if len(part) > 0:
                        if part.count(part[0]) == div and part[0][1] == 1 and str(part[0][0]) in color:
                            line[p:p + div] = [(line[p][0], div)]        
#        
        # Itt cseréli ki a hosszakat érvényes Lego elemkódokra
                    
        for part in range(len(line)):
            for partname in range(len(parts)):
                if line[part][1] == parts.iat[partname,0]:
                    line[part] = (line[part][0], line[part][1], parts.iat[partname,1])
                    
        #  Itt történik meg a tényleges ldr generálása
        x = 0
        for part in range(len(line)):
            color = str(line[part][0])
            x += line[part][1] * 10
            partcode = line[part][2]
            # Minden sorből DataFrame-t generál és hozzáadja az eredeti df-hez
            mlcad_line_df = pd.DataFrame([[color, x, y, inner, partcode]], columns=columns, index = [index])
            index += 1
            mlcad_df = mlcad_df.append(mlcad_line_df)
            # Az mlcad_line-t csak a DataFrame átalakítása után kell összeállítani! Itt több függvény is kell.
#            mlcad_line = "1 " + color + " " + str(x) + " " + str(y) + inner + partcode + "\n"
#            mlcad += mlcad_line
            x += line[part][1] * 10
            
        y += y_step   
    
    
    print img.size[0], "x", img.size[1]
    print cntr, "db alkatrész kell eredetileg"
    print len(mlcad_df), "a redukált alkatrészszám a sorok összevonása után"
    # Működési javaslat: partcode szerint rész df-re vágni és úgy kezelni!
    
   # Kiválasztja a megfelelő függvény(eke)t a bővebb finomításhoz
    
    if tile_plate == False:
        mlcad_df = reduce_with_bricks(mlcad_df, parts)
        mlcad_df = compl_reducer(mlcad_df, parts)
        mlcad_df = reduce_with_bricks(mlcad_df, parts)
        mlcad_df = compl_reducer(mlcad_df, parts)
    else:
        print "csempeszoba"
  
    
    # MlCad fájl sorait összeállító és a fájlt legeneráló rész
    for pos in range(len(mlcad_df)):
        mlcad_line = "1 " + str(mlcad_df.iat[pos,0]) + " " + str(mlcad_df.iat[pos,1]) + " " + str(mlcad_df.iat[pos,2]) + str(mlcad_df.iat[pos,3]) + mlcad_df.iat[pos,4] + "\n"
        mlcad += mlcad_line
    
    mlcad += "0"
    ldr = open(ldr_name, "w")
    ldr.write(mlcad)
    ldr.close()

    mlcad_df.to_csv("mlcad_df.csv")
    
    # Idáig másold át!

# Egymás alatti hármas csoportokat von össze brick-ké, csak alapvető egyezést vizsgál
def reduce_with_bricks(mlcad_df, parts):
    mlcad_df = mlcad_df.sort_values(['x', 'y']).reset_index(drop=True)
    # Iteráció az elemkódokon, majd elemkódok szerint két részre vágja a df-et
    # Végül a törlendő elemeket eldobja, a két részt pedig összeilleszti      
    for rep in range(len(parts)):
        smallplate_df = mlcad_df[mlcad_df['partcode'] == parts.iat[rep,1]]
        useless_df = mlcad_df[mlcad_df['partcode'] != parts.iat[rep,1]]
        for pos in range(len(smallplate_df) - 2):
            if smallplate_df.iat[pos,4] == parts.iat[rep,1]:
                if smallplate_df.iat[pos,2] + 8 == smallplate_df.iat[pos + 1 ,2] and (smallplate_df.iat[pos,2] + 16 == smallplate_df.iat[pos + 2 ,2]):
                    if smallplate_df.iat[pos,1] == smallplate_df.iat[pos + 1 ,1] and (smallplate_df.iat[pos,1] == smallplate_df.iat[pos + 2 ,1]):
                        if smallplate_df.iat[pos,0] == smallplate_df.iat[pos + 1,0] and (smallplate_df.iat[pos,0] == smallplate_df.iat[pos + 2,0]):
                            # HINT: index 3-ról 4-re változik!
                            if smallplate_df.iat[pos,0] in parts.iat[rep,3].split(";"):
                                smallplate_df.iat[pos,4] = parts.iat[rep,2]
                                smallplate_df.iat[pos + 1,4] = "zero"
                                smallplate_df.iat[pos + 2,4] = "zero"
        mlcad_df = smallplate_df.append(useless_df)
        mlcad_df = mlcad_df[mlcad_df['partcode'] != 'zero']
    print len(mlcad_df), "a redukált alkatrészszám a brick-ek beszúrása után"
    return mlcad_df

"""
# TODO: részletesen megírni, EGYSZERŰSÍTENI, SZABÁLYOKAT KERESNI!
# TODO: R E F A C T O R ! ! !
def compl_reducer(mlcad_df, parts):
    for num in range(1,4):
        smallpart = parts.iat[0,1]
        changebrick = parts.iat[0,2]
        bigpart = parts.iat[num,1]
        changepart = parts.iat[num - 1,1]
        x_diff = num * 10
        
        smallplate_df = mlcad_df[mlcad_df['partcode'] == smallpart]
        useless_df = mlcad_df[mlcad_df['partcode'] != smallpart]
        bigplate_df = useless_df[useless_df['partcode'] == bigpart]
        useless_df = useless_df[useless_df['partcode'] != bigpart]
        
        for elem in range(len(smallplate_df)):
            item1_x = smallplate_df.iat[elem,1]
            item1_y = smallplate_df.iat[elem,2]
            item1_color = smallplate_df.iat[elem,0]
            if  smallplate_df.iat[elem,4] == smallpart:
                for in_elem in range(len(smallplate_df)):
                    if smallplate_df.iat[in_elem,4] == smallpart:
                        if smallplate_df.iat[in_elem,0] == item1_color and smallplate_df.iat[in_elem,1] == item1_x and smallplate_df.iat[in_elem,2] - 8 == item1_y:
                            for el in range(len(bigplate_df)):
                                if bigplate_df.iat[el,0] == item1_color:
                                    if bigplate_df.iat[el,4] == bigpart:
                                        if abs(bigplate_df.iat[el,1] - item1_x) == x_diff:
                                            if bigplate_df.iat[el,2] - 16 == item1_y:                           
                                                smallplate_df.iat[elem,4] = "zero" # Ez a zéró mindig zéró!
                                                smallplate_df.iat[in_elem,2] = smallplate_df.iat[in_elem,2] - 8
                                                smallplate_df.iat[in_elem,4] = changebrick
    #                                            bigplate_df.iat[el,4] = "zero"
                                                if bigplate_df.iat[el,1] - item1_x > 0:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + 10
                                                else:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - 10
                                                bigplate_df.iat[el,4] = changepart
    #                                            smallplate_df.iat[in_elem,4] = "zero"
     
        for elem in range(len(smallplate_df)):
            item1_x = smallplate_df.iat[elem,1]
            item1_y = smallplate_df.iat[elem,2]
            item1_color = smallplate_df.iat[elem,0]
            if smallplate_df.iat[elem,4] == smallpart:
                for in_elem in range(len(smallplate_df)):
                    if smallplate_df.iat[in_elem,4] == smallpart:
                        if smallplate_df.iat[in_elem,0] == item1_color and smallplate_df.iat[in_elem,1] == item1_x and smallplate_df.iat[in_elem,2] - 8 == item1_y:
                            for el in range(len(bigplate_df)):
                                if bigplate_df.iat[el,0] == item1_color:
                                    if bigplate_df.iat[el,4] == bigpart:
                                        if abs(bigplate_df.iat[el,1] - item1_x) == x_diff:
                                            if bigplate_df.iat[el,2] + 8 == item1_y:                           
                                                smallplate_df.iat[elem,4] = "zero" # Ez a zéró mindig zéró!
                                                smallplate_df.iat[in_elem,2] = bigplate_df.iat[el,2]
                                                smallplate_df.iat[in_elem,4] = changebrick
    #                                            bigplate_df.iat[el,4] = "zero"
                                                if bigplate_df.iat[el,1] - item1_x > 0:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + 10
                                                else:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - 10
                                                bigplate_df.iat[el,4] = changepart   
    #                                            smallplate_df.iat[in_elem,4] = "zero"
           
        smallplate_df = smallplate_df.append(useless_df)
        mlcad_df = smallplate_df.append(bigplate_df)
        mlcad_df = mlcad_df[mlcad_df['partcode'] != 'zero'] 

    print len(mlcad_df), "a redukált alkatrészszám a bonyolultabb összevonások után"                                                   
    return mlcad_df
"""

# TODO: részletesen megírni, EGYSZERŰSÍTENI, SZABÁLYOKAT KERESNI!
# TODO: R E F A C T O R ! ! !
def compl_reducer(mlcad_df, parts):
    for part in range(0,3):
        for num in range(part + 1,4):
            smallpart = parts.iat[part,1]
            changebrick = parts.iat[part,2]
            bigpart = parts.iat[num,1]
            # Itt van hiba
            changepart = parts.iat[num - (part + 1),1]
            x_diff = (parts.iat[num,0] - parts.iat[part,0]) * 10
            print smallpart, bigpart, part, num
            
            smallplate_df = mlcad_df[mlcad_df['partcode'] == smallpart]
            useless_df = mlcad_df[mlcad_df['partcode'] != smallpart]
            bigplate_df = useless_df[useless_df['partcode'] == bigpart]
            useless_df = useless_df[useless_df['partcode'] != bigpart]
            
            # Ha a nagy elem van alul
            for elem in range(len(smallplate_df)):
                item1_x = smallplate_df.iat[elem,1]
                item1_y = smallplate_df.iat[elem,2]
                item1_color = smallplate_df.iat[elem,0]
                if smallplate_df.iat[elem,4] == smallpart:
                    for in_elem in range(len(smallplate_df)):
                        if smallplate_df.iat[in_elem,4] == smallpart:
                            if smallplate_df.iat[in_elem,0] == item1_color and smallplate_df.iat[in_elem,1] == item1_x and smallplate_df.iat[in_elem,2] - 8 == item1_y:
                                for el in range(len(bigplate_df)):
                                    if bigplate_df.iat[el,0] == item1_color:
                                        if bigplate_df.iat[el,4] == bigpart:
                                            if abs(bigplate_df.iat[el,1] - item1_x) == x_diff:
                                                if bigplate_df.iat[el,2] - 16 == item1_y:                           
                                                    smallplate_df.iat[elem,4] = "zero" # Ez a zéró mindig zéró!
                                                    smallplate_df.iat[in_elem,2] = smallplate_df.iat[in_elem,2] - 8
                                                    smallplate_df.iat[in_elem,4] = changebrick
#                                                    bigplate_df.iat[el,4] = "zero"
                                                    if bigplate_df.iat[el,1] - item1_x > 0:
                                                        bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + (part + 1) * 10
                                                    else:
                                                        bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - (part + 1) * 10
                                                    bigplate_df.iat[el,4] = changepart
#                                                    smallplate_df.iat[in_elem,4] = "zero"
                    
            # Ha a nagy elem van felül
            for elem in range(len(smallplate_df)):
                item1_x = smallplate_df.iat[elem,1]
                item1_y = smallplate_df.iat[elem,2]
                item1_color = smallplate_df.iat[elem,0]
                if smallplate_df.iat[elem,4] == smallpart:
                    for in_elem in range(len(smallplate_df)):
                        if smallplate_df.iat[in_elem,4] == smallpart:
                            if smallplate_df.iat[in_elem,0] == item1_color and smallplate_df.iat[in_elem,1] == item1_x and smallplate_df.iat[in_elem,2] - 8 == item1_y:
                                for el in range(len(bigplate_df)):
                                    if bigplate_df.iat[el,0] == item1_color:
                                        if bigplate_df.iat[el,4] == bigpart:
                                            if abs(bigplate_df.iat[el,1] - item1_x) == x_diff:
                                                if bigplate_df.iat[el,2] + 8 == item1_y:                           
                                                    smallplate_df.iat[elem,4] = "zero" # Ez a zéró mindig zéró!
                                                    smallplate_df.iat[in_elem,2] = bigplate_df.iat[el,2]
                                                    smallplate_df.iat[in_elem,4] = changebrick
#                                                    bigplate_df.iat[el,4] = "zero"
                                                    if bigplate_df.iat[el,1] - item1_x > 0:
                                                        bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + (part + 1) * 10
                                                    else:
                                                        bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - (part + 1) * 10
                                                    bigplate_df.iat[el,4] = changepart   
#                                                    smallplate_df.iat[in_elem,4] = "zero"
             
            # Ha a nagy elem van középen
            for elem in range(len(smallplate_df)):
                item1_x = smallplate_df.iat[elem,1]
                item1_y = smallplate_df.iat[elem,2]
                item1_color = smallplate_df.iat[elem,0]
                if smallplate_df.iat[elem,4] == smallpart:
                    for in_elem in range(len(smallplate_df)):
                        if smallplate_df.iat[in_elem,4] == smallpart:
                            if smallplate_df.iat[in_elem,0] == item1_color and smallplate_df.iat[in_elem,1] == item1_x and smallplate_df.iat[in_elem,2] - 16 == item1_y:
                                for el in range(len(bigplate_df)):
                                    if bigplate_df.iat[el,0] == item1_color:
                                        if bigplate_df.iat[el,4] == bigpart:
                                            if abs(bigplate_df.iat[el,1] - item1_x) == x_diff:
                                                if bigplate_df.iat[el,2] - 8 == item1_y:                           
                                                    smallplate_df.iat[elem,4] = "zero" # Ez a zéró mindig zéró!
                                                    smallplate_df.iat[in_elem,2] = bigplate_df.iat[el,2] - 8
                                                    smallplate_df.iat[in_elem,4] = changebrick
#                                                    bigplate_df.iat[el,4] = "zero"
                                                    if bigplate_df.iat[el,1] - item1_x > 0:
                                                        bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + (part + 1) * 10
                                                    else:
                                                        bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - (part + 1) * 10
                                                    bigplate_df.iat[el,4] = changepart   
#                                                    smallplate_df.iat[in_elem,4] = "zero"
            
            smallplate_df = smallplate_df.append(useless_df)
            mlcad_df = smallplate_df.append(bigplate_df)
            mlcad_df = mlcad_df[mlcad_df['partcode'] != 'zero'] 

    print len(mlcad_df), "a redukált alkatrészszám a bonyolultabb összevonások után"                                                   
    return mlcad_df

"""

# Függvény, ami beolvassa a már legenerált képfájlt és elkészíti a redukált alkatrészlistát / MlCad fájlt
def reduce_partlist(filename, img, plate_wid, plate_height, tile_plate):
    print plate_wid, plate_height
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
    
    
    y = 0
    
    # MlCad DataFrame inicializálása
    columns = ['color', 'x', 'y', 'inner', 'partcode']
    mlcad_df = pd.DataFrame(columns=columns)
    index = 0    
    
    for j in range(0,img.size[1],plate_height):
        for i in range(0,img.size[0],plate_wid):
            picture.append((pixels[i,j], 1))
            cntr += 1
    for item in range(0,len(picture), num_wid):
        line = picture[item: item + num_wid]
        # Original color/ part pairs from file
        divs = []
        f = open("original_plates.col", "r")
        original_colors = f.read()
        f.close()
        original_colors = original_colors.split("\n")
        for color_line in original_colors:
            color_codes = ()
            for  color_code in color_line.split("  ")[1].split(" "):
                color_codes += (int(color_code),)
            divs.append((int(color_line.split("  ")[0]), (color_codes)))        
        
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
        
        for part in range(len(line)):
            # Itt cseréli ki a hosszakat érvényes Lego elemkódokra
            for partname in range(len(parts)):
                if line[part][1] == parts[partname][0]:
                    line[part] = (line[part][0], line[part][1], parts[partname][1])
        #  Itt történik meg a tényleges ldr generálása
        x = 0
        for part in range(len(line)):
            color = str(line[part][0])
            x += line[part][1] * 10
            partcode = line[part][2]
            # Minden sorből DataFrame-t generál és hozzáadja az eredeti df-hez
            mlcad_line_df = pd.DataFrame([[color, x, y, inner, partcode]], columns=columns, index = [index])
            index += 1
            mlcad_df = mlcad_df.append(mlcad_line_df)
            x += line[part][1] * 10
            
        y += y_step   
           
    # Itt áll rendelkezésre az egész df, innentől kell redukálni!
    mlcad_df = mlcad_df.sort_values(['x', 'y']).reset_index(drop=True)
    
    print img.size[0], "x", img.size[1]
    print cntr, "db alkatrész kell eredetileg"
    print len(mlcad_df), "a redukált alkatrészszám a sorok összevonása után"
    # Működési javaslat: partcode szerint rész df-re vágni és úgy kezelni!
    
   # Kiválasztja a megfelelő függvény(eke)t a bővebb finomításhoz
    if tile_plate == False:
        mlcad_df = reduce_with_bricks(mlcad_df)
        # TODO: pattern search
    else:
        # TODO: csempefelosztó fv.
        print "csempeszoba"
  
    # MlCad fájl sorait összeállító és a fájlt legeneráló rész
    for pos in range(len(mlcad_df)):
        mlcad_line = "1 " + str(mlcad_df.iat[pos,0]) + " " + str(mlcad_df.iat[pos,1]) + " " + str(mlcad_df.iat[pos,2]) + str(mlcad_df.iat[pos,3]) + mlcad_df.iat[pos,4] + "\n"
        mlcad += mlcad_line
    
    mlcad += "0"
    print len(mlcad_df), "a redukált alkatrészszám"
    ldr = open(ldr_name, "w")
    ldr.write(mlcad)
    ldr.close()
    
# Egymás alatti hármas csoportokat von össze brick-ké, csak alapvető egyezést vizsgál
def reduce_with_bricks(mlcad_df):
    # Feltöltés valós brick/color értékekkel, megfelelő formára hozás
    # TODO: valós szín rendelkezésre állást ellenőrizni!
    replace_parts = []
    f = open("original_bricks.col", "r")
    original_brick_colors = f.read()
    f.close()
    original_brick_colors = original_brick_colors.split("\n")
    for brick_color_line in original_brick_colors:
        brick_color_codes = ()
        for  brick_color_code in brick_color_line.split("  ")[1].split(" "):
            brick_color_codes += (int(brick_color_code),)
        replace_parts.append((brick_color_line.split("  ")[0].split(" ")[0], brick_color_line.split("  ")[0].split(" ")[1], (brick_color_codes)))

    # Iteráció az elemkódokon, majd elemkódok szerint két részre vágja a df-et
    # Végül a törlendő elemeket eldobja, a két részt pedig összeilleszti      
    for rep in range(len(replace_parts)):
        part1_mlcad_df = mlcad_df[mlcad_df['partcode'] == replace_parts[rep][1]]
        part2_mlcad_df = mlcad_df[mlcad_df['partcode'] != replace_parts[rep][1]]
        for pos in range(len(part1_mlcad_df) - 2):
            if part1_mlcad_df.iat[pos,4] == replace_parts[rep][1]:
                if part1_mlcad_df.iat[pos,2] + 8 == part1_mlcad_df.iat[pos + 1 ,2] and (part1_mlcad_df.iat[pos,2] + 16 == part1_mlcad_df.iat[pos + 2 ,2]):
                    if part1_mlcad_df.iat[pos,1] == part1_mlcad_df.iat[pos + 1 ,1] and (part1_mlcad_df.iat[pos,1] == part1_mlcad_df.iat[pos + 2 ,1]):
                        if part1_mlcad_df.iat[pos,0] == part1_mlcad_df.iat[pos + 1,0] and (part1_mlcad_df.iat[pos,0] == part1_mlcad_df.iat[pos + 2,0]):
                            if int(part1_mlcad_df.iat[pos,0]) in replace_parts[rep][2]:
                                part1_mlcad_df.iat[pos,4] = replace_parts[rep][0]
                                part1_mlcad_df.iat[pos + 1,4] = "zero"
                                part1_mlcad_df.iat[pos + 2,4] = "zero"
        mlcad_df = part1_mlcad_df.append(part2_mlcad_df)
        mlcad_df = mlcad_df[mlcad_df['partcode'] != 'zero']
    return mlcad_df
"""