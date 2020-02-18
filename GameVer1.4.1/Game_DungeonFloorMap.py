#  _____                                        _____                           _
# |  __ \                                      / ____|                         | |
# | |  | |_   _ _ __   __ _  ___  ___  _ __   | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __
# | |  | | | | | '_ \ / _` |/ _ \/ _ \| '_ \  | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
# | |__| | |_| | | | | (_| |  __/ (_) | | | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |
# |_____/ \__,_|_| |_|\__, |\___|\___/|_| |_|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|
#                      __/ |
#                     |___/


import random
from random import choice
TILES = {'fill_tile': '#',
         'floor': '0',
         'wall': '1'}

floor_array = []
location = 0
roomList = []
corridorList = []


def change_char(s, p, r):
    return s[:p] + r + s[p + 1:]


class Generator():
    def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5,
                 max_room_xy=10, rooms_overlap=False, random_connections=1,
                 random_spurs=1, tiles=TILES):
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_xy = min_room_xy
        self.max_room_xy = max_room_xy
        self.rooms_overlap = rooms_overlap
        self.random_connections = random_connections
        self.random_spurs = random_spurs
        self.tiles = TILES
        self.level = []
        self.room_list = []
        self.corridor_list = []
        self.tiles_level = []

    def gen_room(self):
        x, y, w, h = 0, 0, 0, 0

        w = random.randint(self.min_room_xy, self.max_room_xy)
        h = random.randint(self.min_room_xy, self.max_room_xy)
        x = random.randint(1, (self.width - w - 1))
        y = random.randint(1, (self.height - h - 1))

        return [x, y, w, h]

    def room_overlapping(self, room, room_list):

        roomx, roomy, roomw, roomh = room[0], room[1], room[2], room[3]

        graph = [[0] * self.width for _ in range(self.height)]

        for i in room_list:

            XC, YC, WL, HL = i[0], i[1], i[2], i[3]
            padx, pady = 1, 1

            # graph[y][x]: [y][x + w] <---- Logic
            if XC + WL + 3 <= self.width:
                padx = 3
            for x in range(XC - padx - 1, XC + WL + padx):
                if YC + HL + 3 <= self.height:
                    pady = 3
                for y in range(YC - pady - 1, YC + HL + pady):
                    graph[y][x] = 1

        for xl in range(roomx, roomx + roomw):
            for yl in range(roomy, roomy + roomh):
                if graph[yl][xl] == 1:
                    return True

        return False

    def corridor_between_points(self, x1, y1, x2, y2, join_type='either'):
        if x1 == x2 and y1 == y2 or x1 == x2 or y1 == y2:
            return [(x1, y1), (x2, y2)]
        else:
            # 2 Corridors
            # NOTE: Never randomly choose a join that will go out of bounds
            # when the walls are added.
            join = None
            if join_type is 'either' and set([0, 1]).intersection(
                    set([x1, x2, y1, y2])):

                join = 'bottom'
            elif join_type is 'either' and set([self.width - 1,
                                                self.width - 2]).intersection(set([x1, x2])) or set(
                [self.height - 1, self.height - 2]).intersection(
                set([y1, y2])):

                join = 'top'
            elif join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join is 'top':
                return [(x1, y1), (x1, y2), (x2, y2)]
            elif join is 'bottom':
                return [(x1, y1), (x2, y1), (x2, y2)]

    def join_rooms(self, room_1, room_2, join_type='either'):
        # sort by the value of x
        sorted_room = [room_1, room_2]
        sorted_room.sort(key=lambda x_y: x_y[0])

        x1 = sorted_room[0][0]
        y1 = sorted_room[0][1]
        w1 = sorted_room[0][2]
        h1 = sorted_room[0][3]
        x1_2 = x1 + w1 - 1
        y1_2 = y1 + h1 - 1

        x2 = sorted_room[1][0]
        y2 = sorted_room[1][1]
        w2 = sorted_room[1][2]
        h2 = sorted_room[1][3]
        x2_2 = x2 + w2 - 1
        y2_2 = y2 + h2 - 1

        # overlapping on x
        if x1 < (x2 + w2) and x2 < (x1 + w1):
            jx1 = random.randint(x2, x1_2)
            jx2 = jx1
            tmp_y = [y1, y2, y1_2, y2_2]
            tmp_y.sort()
            jy1 = tmp_y[1] + 1
            jy2 = tmp_y[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # overlapping on y
        elif y1 < (y2 + h2) and y2 < (y1 + h1):
            if y2 > y1:
                jy1 = random.randint(y2, y1_2)
                jy2 = jy1
            else:
                jy1 = random.randint(y1, y2_2)
                jy2 = jy1
            tmp_x = [x1, x2, x1_2, x2_2]
            tmp_x.sort()
            jx1 = tmp_x[1] + 1
            jx2 = tmp_x[2] - 1

            corridors = self.corridor_between_points(jx1, jy1, jx2, jy2)
            self.corridor_list.append(corridors)

        # no overlap
        else:
            join = None
            if join_type is 'either':
                join = random.choice(['top', 'bottom'])
            else:
                join = join_type

            if join is 'top':
                if y2 > y1:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2 - 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1 - 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)

            elif join is 'bottom':
                if y2 > y1:
                    jx1 = random.randint(x1, x1_2)
                    jy1 = y1_2 + 1
                    jx2 = x2 - 1
                    jy2 = random.randint(y2, y2_2)
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'top')
                    self.corridor_list.append(corridors)
                else:
                    jx1 = x1_2 + 1
                    jy1 = random.randint(y1, y1_2)
                    jx2 = random.randint(x2, x2_2)
                    jy2 = y2_2 + 1
                    corridors = self.corridor_between_points(
                        jx1, jy1, jx2, jy2, 'bottom')
                    self.corridor_list.append(corridors)

    def gen_level(self):

        # build an empty dungeon, blank the room and corridor lists
        for i in range(self.height):
            self.level.append(['fill_tile'] * self.width)
        self.room_list = []
        self.corridor_list = []

        max_iters = self.max_rooms * 5

        for a in range(max_iters):
            tmp_room = self.gen_room()

            if self.rooms_overlap or not self.room_list:
                self.room_list.append(tmp_room)
            else:
                tmp_room = self.gen_room()
                tmp_room_list = self.room_list[:]

                if self.room_overlapping(tmp_room, tmp_room_list) is False:
                    self.room_list.append(tmp_room)

            if len(self.room_list) >= self.max_rooms:
                break

        # connect the rooms
        for a in range(len(self.room_list) - 1):
            self.join_rooms(self.room_list[a], self.room_list[a + 1])

        # do the random joins
        for a in range(self.random_connections):
            room_1 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # do the spurs
        for a in range(self.random_spurs):
            room_1 = [random.randint(2, self.width - 2), random.randint(
                2, self.height - 2), 1, 1]
            room_2 = self.room_list[random.randint(0, len(self.room_list) - 1)]
            self.join_rooms(room_1, room_2)

        # fill the map
        # paint rooms
        for room_num, room in enumerate(self.room_list):
            for b in range(room[2]):
                for c in range(room[3]):
                    self.level[room[1] + c][room[0] + b] = 'floor'

        # paint corridors
        for corridor in self.corridor_list:
            x1, y1 = corridor[0]
            x2, y2 = corridor[1]
            for width in range(abs(x1 - x2) + 1):
                for height in range(abs(y1 - y2) + 1):
                    self.level[min(y1, y2) + height][
                        min(x1, x2) + width] = 'floor'

            if len(corridor) == 3:
                x3, y3 = corridor[2]

                for width in range(abs(x2 - x3) + 1):
                    for height in range(abs(y2 - y3) + 1):
                        self.level[min(y2, y3) + height][
                            min(x2, x3) + width] = 'floor'

        # paint the walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                if self.level[row][col] == 'floor':
                    if self.level[row - 1][col - 1] == 'fill_tile':
                        self.level[row - 1][col - 1] = 'wall'

                    if self.level[row - 1][col] == 'fill_tile':
                        self.level[row - 1][col] = 'wall'

                    if self.level[row - 1][col + 1] == 'fill_tile':
                        self.level[row - 1][col + 1] = 'wall'

                    if self.level[row][col - 1] == 'fill_tile':
                        self.level[row][col - 1] = 'wall'

                    if self.level[row][col + 1] == 'fill_tile':
                        self.level[row][col + 1] = 'wall'

                    if self.level[row + 1][col - 1] == 'fill_tile':
                        self.level[row + 1][col - 1] = 'wall'

                    if self.level[row + 1][col] == 'fill_tile':
                        self.level[row + 1][col] = 'wall'

                    if self.level[row + 1][col + 1] == 'fill_tile':
                        self.level[row + 1][col + 1] = 'wall'

    def gen_tiles_level(self):

        for row_num, row in enumerate(self.level):
            tmp_tiles = []

            for col_num, col in enumerate(row):
                if col == 'fill_tile':
                    tmp_tiles.append(self.tiles['fill_tile'])
                if col == 'floor':
                    tmp_tiles.append(self.tiles['floor'])
                if col == 'wall':
                    tmp_tiles.append(self.tiles['wall'])

            self.tiles_level.append(''.join(tmp_tiles))

        ##        print('Room List: ', self.room_list)
        ##        print('\nCorridor List: ', self.corridor_list)

        # Padding sides with #
        [floor_array.append("#" + row + "#") for row in self.tiles_level]
        # [floor_array.append(row) for row in self.tiles_level]


        floor_array.insert(0, (len(floor_array[0]) * "#"))

        floor_array.insert(len(floor_array), (len(floor_array[0]) * "#"))

        #roomList.append(self.room_list)
        #corridorList.append(self.corridor_list)

    def RandLocal(self):
        Room = (choice(self.room_list))
        #print(Room)
        # print(coords)
        location = random.randint(Room[0] + 2, Room[0] + Room[2] - 2),\
                   random.randint(Room[1] +2 , Room[1] + Room[3] - 2)

        # print(location, coords, xPlus, yPlus)
        # print(floor_array[location[1]])
        #print(location)
        #floor_array[location[1]] = change_char(floor_array[location[1]], location[0] - 1, "P")  # placeholder
        return location
        # print(floor_array[location[1]] + "\n")

#  _____       _ _   _       _ _            ______
# |_   _|     (_) | (_)     | (_)          |  ____|
#   | |  _ __  _| |_ _  __ _| |_ ___  ___  | |__ _   _ _ __   ___
#   | | | '_ \| | __| |/ _` | | / __|/ _ \ |  __| | | | '_ \ / __|
#  _| |_| | | | | |_| | (_| | | \__ \  __/ | |  | |_| | | | | (__
# |_____|_| |_|_|\__|_|\__,_|_|_|___/\___| |_|   \__,_|_| |_|\___|
#

def Create_FloorMap(size):
    # Belongs to Legacy Code
    # Defaults -----> width=64, height=64, max_rooms=15, min_room_xy=5, max_room_xy=10
    # Remove Bracket Values to reset to defaults
    MaxRoom, MinSize, MaxSize = 0, 0, 0

    # Key word Value Assignment:
    # Small, Medium_Small, Medium, Medium_Large, Large, Huge, Gigantic, Extreme
    # Represented by representative letters
    # S -----> MS -----> M -----> ML -----> L -----> H -----> G -----> E
    if size == 'S':
        size = 32
        MaxRoom, MinSize, MaxSize = 5, 5, 8

    elif size == 'MS':
        size = 48
        MaxRoom, MinSize, MaxSize = 10, 5, 8

    elif size == 'M':
        size = 64
        MaxRoom, MinSize, MaxSize = 15, 5, 10

    elif size == 'ML':
        size = 96
        MaxRoom, MinSize, MaxSize = 15, 10, 12

    elif size == 'L':
        size = 144
        MaxRoom, MinSize, MaxSize = 20, 10, 12

    elif size == 'H':
        size = 216
        MaxRoom, MinSize, MaxSize = 40, 5, 15

    elif size == 'G':
        size = 324
        MaxRoom, MinSize, MaxSize = 50, 5, 15

    elif size == 'E':
        size = 486
        MaxRoom, MinSize, MaxSize = 60, 5, 20

    gen = Generator(size, size, MaxRoom, MinSize, MaxSize)
    gen.gen_level()
    gen.gen_tiles_level()
    Stairs = gen.RandLocal()
    Start = gen.RandLocal()
    rooms = gen.room_list
    return floor_array, len(floor_array), len(floor_array[0]), Stairs, Start, rooms

# Test Each variant
#[print(i) for i in Create_FloorMap('S')[0]]
# [print(i) for i in Create_FloorMap('MS')[0]]
# [print(i) for i in Create_FloorMap('M')[0]]
# [print(i) for i in Create_FloorMap('ML')[0]]
# [print(i) for i in Create_FloorMap('L')[0]]
# [print(i) for i in Create_FloorMap('H')[0]]
# [print(i) for i in Create_FloorMap('G')[0]]
# [print(i) for i in Create_FloorMap('E')[0]]
#print(Create_FloorMap('S'))




