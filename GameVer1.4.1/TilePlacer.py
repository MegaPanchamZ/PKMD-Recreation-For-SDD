import Game_DungeonFloorMap as GDFM
from random import choice

#MAP = GDFM.Create_FloorMap('S')[0]

##file = open("TrialMap.txt", "r")
##MAP = []
##[MAP.append(row) for row in file]

def cardinal_dir(tile, tileloc,location, array):
    TileCombs = {'#11#': '408','#011': '58','#1#1': '409','11#0': '30',
                 '1010': '57','0#11': '4','0110': '3','1##1': '436',
                 '1#1#': '435','110#': '32','0111': '4','1001': '59',
                 '0101': '5','#111': '328','0001': '194','1011': '58',
                 '1110': '30','0010': '192','1100': '111','1#11': '382',
                 '1101': '32','111#': '356','1111': '193','11#1': '354',
                 '0011': '85','0100': '166','1000': '220','0000': '112',
                 '0#01': '84'}
    #TL = tile location
    TL = location,tileloc
    #top, bot, RT, LT
    #print(tile, tileloc, location)
    top = array[TL[0]-1][TL[1]]
    bot = array[TL[0]+1][TL[1]]
    RT = array[TL[0]][TL[1]+1]
    LT =  array[TL[0]][TL[1]-1]
    #print(top+ bot+ RT+LT)
    return TileCombs[top+ bot+ RT+LT]
    

def tileGen(array):
    newmap = []
    Solid = ["31","31","31","31","31","31","31","31","31","31","31","31","31",
             "31","31","31","31","31","31","31","31","31","31","31","31","31",
             "31","31","31","31","31","31","31","31","31","31","31","31","31",
             "31","31","31","31","31","31","31","31","31","31","31","31","31",
             "34", "37"]
    Ground = ["12", '13', '14', '41','40','40','40','40','40','40','40','40',
              '40','40','40','40','40','40','40','40','40','40','40','40','40',
              '40','40','40','40','40','40','40','40','40','40','40','40','40',
              '40','40','40','40','40','40','40','40','40','40','40','40','40',
              '40','40','40','40','40','40','40','40','40','40','40','40','40',
              '40','40','40','40','40','40','40','40','40','40','40','40','40',
              '40','40','40','40','40','40','40','40','40','40','40','40','40',
              '39','66','67','68','93','94','95','120','40','40','121','147',
              '149','149','175','201','202','203']
    count = -1
    for item in array:
        count += 1
        store = []
        locCount = -1
        for element in item:
            locCount += 1
            if element == '1':
                store.append(cardinal_dir(element, locCount, count, array))
            elif element != "\n":
                if element == "0":
                    store.append(choice(Ground))
                if element == "#":
                    store.append(choice(Solid))
        #print(store)
        newmap.append([store])
    #print(newmap)
    return newmap

# Master Function

def initial(size):
    MB = []
    mapdata = GDFM.Create_FloorMap(size)
    [MB.append(i[0]) for i in tileGen(mapdata[0])]
    return MB, mapdata

# Code below tests all possible tile enviroments Add new tile ID
#Add new tile ID if console prints statement. Key is given as output.
'''
count = 0
while True:
    count = count + 1
    for i in tileGen(GDFM.Create_FloorMap('M')[0]):

        for e in i:
            for n in e:
                if n in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                    print("Continue Combinations" + "Found: " + n)
    #Uncomment to notify if new map is generated
    print("NewMap" + ': ' + str(count))
'''