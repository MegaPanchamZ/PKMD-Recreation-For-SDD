import pygame as pg
import xml.etree.ElementTree as ET
import os

pg.init()
pg.display.set_mode((20, 20))


currentfolder = os.path.dirname(__file__)

def get_image_rect(sheet, x, y, w, h):
    # print(x,y,w,h)
    return sheet.subsurface(pg.Rect(x, y, w, h))

def splitter(Folder, Sheet, DataFile):
    try:
        Sheet = pg.image.load(Sheet).convert_alpha()
    except pg.error as message:
        return
    XML = DataFile
    tree = ET.parse(XML)
    root = tree.getroot()
    for item in root:
        if item.tag == "FrameWidth":
            framewidth = int(item.text)
        if item.tag == "FrameHeight":
            frameheight = int(item.text)


    width = int(Sheet.get_rect().size[0] / framewidth)

    height = int(Sheet.get_rect().size[1] / frameheight)

    #print(width, height)

    
    img_range = width*height
    
    for i in range(img_range):   
        row = int(i / width)
        col = i % width
        y, x = row * frameheight, col * framewidth

        #print(x,y)
        pg.image.save(get_image_rect(Sheet, x, y, framewidth, frameheight), (Folder + str(i) + ".png"))
        #print(Folder)
    

#splitter()
sheet = ''
xml = ''

for folder in os.listdir(currentfolder):
    print(folder)
    for file in os.listdir(folder):
        if file.endswith('.png'):
            sheet = currentfolder + "/" + folder + "/" + file
            
        if file.endswith('.xml'):
            xml = currentfolder + "/" + folder + "/" + file

    splitter((currentfolder + "/" + folder + "/"), sheet, xml)
        #print(sheet, xml)
        #print(os.path.join(currentfolder, file))
            


#for i in list_anims:
#   pg.image.save(i, "donky.png")

