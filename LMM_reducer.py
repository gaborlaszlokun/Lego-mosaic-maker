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
import pandas as pd

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
        
        # Eredeti Lego part/color betöltése
        # HINT: lehetne globális(abb)
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
        
        # Itt cseréli sorfolytonosan az elemeket nagyobbakra, ha az adott színű elem létezik
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
#        print len(line), item / num_wid
        
        # Itt cseréli ki a hosszakat érvényes Lego elemkódokra
        for part in range(len(line)):
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
        mlcad_df = reduce_with_bricks(mlcad_df)
        mlcad_df = compl_reducer(mlcad_df, parts)
        mlcad_df = reduce_with_bricks(mlcad_df)
        mlcad_df = compl_reducer(mlcad_df, parts)
    else:
        print "csempeszoba"
  
    # MlCad fájl sorait összeállító és a fájlt legeneráló rész
    for pos in range(len(mlcad_df)):
        mlcad_line = "1 " + str(mlcad_df.iat[pos,0]) + " " + str(mlcad_df.iat[pos,1]) + " " + str(mlcad_df.iat[pos,2]) + str(mlcad_df.iat[pos,3]) + mlcad_df.iat[pos,4] + "\n"
        mlcad += mlcad_line
    
    mlcad += "0"
    ldr = open("new_" + ldr_name, "w")
    ldr.write(mlcad)
    ldr.close()

    mlcad_df.to_csv("mlcad_df.csv")
    
    # Idáig másold át!

# Egymás alatti hármas csoportokat von össze brick-ké, csak alapvető egyezést vizsgál
def reduce_with_bricks(mlcad_df):
    # Feltöltés valós brick/color értékekkel, megfelelő formára hozás
    # HINT: lehetne globális/paraméter!
    mlcad_df = mlcad_df.sort_values(['x', 'y']).reset_index(drop=True)
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
        smallplate_df = mlcad_df[mlcad_df['partcode'] == replace_parts[rep][1]]
        useless_df = mlcad_df[mlcad_df['partcode'] != replace_parts[rep][1]]
        for pos in range(len(smallplate_df) - 2):
            if smallplate_df.iat[pos,4] == replace_parts[rep][1]:
                if smallplate_df.iat[pos,2] + 8 == smallplate_df.iat[pos + 1 ,2] and (smallplate_df.iat[pos,2] + 16 == smallplate_df.iat[pos + 2 ,2]):
                    if smallplate_df.iat[pos,1] == smallplate_df.iat[pos + 1 ,1] and (smallplate_df.iat[pos,1] == smallplate_df.iat[pos + 2 ,1]):
                        if smallplate_df.iat[pos,0] == smallplate_df.iat[pos + 1,0] and (smallplate_df.iat[pos,0] == smallplate_df.iat[pos + 2,0]):
                            if int(smallplate_df.iat[pos,0]) in replace_parts[rep][2]:
                                smallplate_df.iat[pos,4] = replace_parts[rep][0]
                                smallplate_df.iat[pos + 1,4] = "zero"
                                smallplate_df.iat[pos + 2,4] = "zero"
        mlcad_df = smallplate_df.append(useless_df)
        mlcad_df = mlcad_df[mlcad_df['partcode'] != 'zero']
    print len(mlcad_df), "a redukált alkatrészszám a brick-ek beszúrása után"
    return mlcad_df


# TODO: részletesen megírni, EGYSZERŰSÍTENI, SZABÁLYOKAT KERESNI!
# TODO: R E F A C T O R ! ! !
def compl_reducer(mlcad_df, parts):
    for num in range(1,4):
        smallpart = parts[0][1]
        bigpart = parts[num][1]
        changepart = parts[num - 1][1]
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
                                                smallplate_df.iat[in_elem,4] = "3005.dat"
    #                                            bigplate_df.iat[el,4] = "zero"
                                                if bigplate_df.iat[el,1] - item1_x > 0:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + 10
                                                else:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - 10
                                                bigplate_df.iat[el,4] = changepart
    #                                            smallplate_df.iat[in_elem,4] = "zero"
                                                
#                                                print bigpart, "csere", bigplate_df.iat[el,0], " a szín"
                                                                    
     
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
    #                                            smallplate_df.iat[elem,4] = "zero" # Ez a zéró mindig zéró!
                                                smallplate_df.iat[in_elem,2] = bigplate_df.iat[el,2]
                                                smallplate_df.iat[in_elem,4] = "3005.dat"
    #                                            bigplate_df.iat[el,4] = "zero"
                                                if bigplate_df.iat[el,1] - item1_x > 0:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] + 10
                                                else:
                                                    bigplate_df.iat[el,1] = bigplate_df.iat[el,1] - 10
                                                bigplate_df.iat[el,4] = changepart   
    #                                            smallplate_df.iat[in_elem,4] = "zero"
                                                
#                                                print bigpart, "csere", bigplate_df.iat[el,0], " a szín"
           
        smallplate_df = smallplate_df.append(useless_df)
        mlcad_df = smallplate_df.append(bigplate_df)
        mlcad_df = mlcad_df[mlcad_df['partcode'] != 'zero'] 

    print len(mlcad_df), "a redukált alkatrészszám a bonyolultabb összevonások után"                                                   
    return mlcad_df


# Usage
img = "plate_30_kimi.jpg"
reduce_partlist(img, 30, 12, False)

#img = "plate_40_albert.jpg"
#reduce_partlist(img, 15, 6, False)

#img = "tile_20_me.jpg"
#reduce_partlist(img, 30, 30, True)