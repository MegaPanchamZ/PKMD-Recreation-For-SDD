
import Game_DungeonFloorMap as GDFM


tmap = GDFM.Create_FloorMap()

roomCoords = tmap[2][0]
pathCoords = tmap[3][0]
pathlist = []

#Debug see whole map.
#[print(i) for i in tmap[0]]

#Debug See Co-Ordinates for rooms and corridors.
#Stored in nested lists
for i in roomCoords:
    i[0] = i[0] + 1
    i[1] = i[1] + 1

for i in pathCoords:
    store = []
    for e in i:
        if len(store) < len(i):
            e = list(e)
            e[0] = e[0] + 1
            e[1] = e[1] + 1
            store.append(e)
    pathlist.append(store)
pathCoords = pathlist

def change_char(s, p, r):
    return s[:p] + r + s[p + 1:]

def CornerDefiner(roomCoords):
    TL = []
    TR = []
    BL = []
    BR = []

    for item in roomCoords:
        #X, Y
        TL.append([item[0]-1, item[1]-1])
        TR.append([item[0]+item[2], item[1]-1])
        BL.append([item[0]-1, item[1] + item[3]])
        BR.append([item[0]+ item[2], item[1]+item[3]])

    return TL, TR, BL, BR

def Swap(CornerLocations):
    Cl = CornerLocations
    for i in Cl[0]:
        tmap[0][i[1]] = change_char(tmap[0][i[1]], i[0], 'C')

    for i in Cl[1]:
        tmap[0][i[1]] = change_char(tmap[0][i[1]], i[0], 'C')

    for i in Cl[2]:
        tmap[0][i[1]] = change_char(tmap[0][i[1]], i[0], 'C')

    for i in Cl[3]:
        tmap[0][i[1]] = change_char(tmap[0][i[1]], i[0], 'C')

    return(tmap[0])



def initiate_map():
    MAP = Swap(CornerDefiner(roomCoords))
    return MAP

#Debug Statement Prints out in console (Map)
#[print(i) for i in tmap[0]]

