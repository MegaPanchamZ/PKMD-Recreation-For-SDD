import Game_DungeonFloorMap as GDFM
from random import choice

MAP = GDFM.Create_FloorMap()[0]

##file = open("TrialMap.txt", "r")
##MAP = []
##[MAP.append(row) for row in file]

def cardinal_dir(tile, tileloc,location, array):
    TileCombs = {'#11#': '453','#011': '64','#1#1': '454','11#0': '33',
                 '1010': '63','0#11': '4','0110': '3','1##1': '484',
                 '1#1#': '483','110#': '35','0111': '274','1001': '153',
                 '0101': '93','#111': '364','0001': '213','1011': '334',
                 '1110': '305','0010': '215','1100': '123','1#11': '424',
                 '1101': '303','111#': '395','1111': '214','11#1': '393',
                 '0011': '94','0100': '184','1000': '244','0000': '124',
                 '100#': '603','010#': '574','0#1#': '274','####': '37',
                 '###1': '393','###0': '35','##1#': '395','##11': '214',
                 '##10': '544','##0#': '395','##01': '543','##00': '123',
                 '#1##': 'A','#1#0': 'B','#110': 'C','#10#': 'D',
                 '#101': 'E','#100': 'F','#0##': 'G','#0#1': 'H',
                 '#0#0': 'I','#01#': 'J','#010': 'K','#00#': 'L',
                 '#001': 'M','#000': 'N','1###': 'O',
                 '1##0': 'Q','1#10': 'R','1#0#': 'S','1#01': 'T',
                 '1#00': 'U','11##': 'V','10##': 'W','10#1': 'X',
                 '10#0': 'Y','101#': 'Z','0###': 'a','0##1': 'b',
                 '0##0': 'c','0#10': '574','0#0#': '633','0#01': 'f',
                 '0#00': 'g','01##': 'h','01#1': 'i','01#0': 'j',
                 '011#': 'k','00##': 'm','00#1': 'n',
                 '00#0': 'o','001#': '94','000#': 'q'}
    #TL = tile location
    TL = location,tileloc
    #top, bot, RT, LT
    top, bot = array[TL[0]-1][TL[1]], array[TL[0]+1][TL[1]]
    RT, LT = array[TL[0]][TL[1]+1], array[TL[0]][TL[1]-1]
    #print(top+ bot+ RT+LT)
    return TileCombs[top+ bot+ RT+LT]
    

def tileGen(array):
    newmap = []
    Solid = ["34", "37", "40"]
    Ground = ["12", '13', '14', '42', '43', '44', '46', '49',
              '52', '72', '73', '74','102', '103', '104', '132',
              '133', '162', '164', '193', '222', '223', '224',
              '253', '283', '312', '314', '343', '373', '402',
              '404', '433', '462', '463', '49', '493', '522',
              '523', '552', '553', '582', '583', '612', '613',
              '642', '643', '672', '673', '702', '703']
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
        store = [",".join(store)]
        newmap.append(store)

    return newmap

#Master Function

def initial(size):
    MB = []
    [MB.append(i[0]) for i in tileGen(GDFM.Create_FloorMap(size)[0])]
    return MB


# Code below tests all possible tile enviroments Add new tile ID
#Add new tile ID if console prints statement. Key is given as output.
'''
while True:
    for i in tileGen(MAP):
        for e in i:
            for n in e:
                if n in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
                    print("F found Continue Combinations" + "Found: " + n)
    #Uncomment to notify if new map is generated
    #print("NewMap")
'''
    
