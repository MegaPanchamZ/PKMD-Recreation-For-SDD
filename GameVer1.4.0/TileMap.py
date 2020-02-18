import pygame as pg
import Game_DungeonFloorMap as GDFM
import TilePlacer as tp
from settings import *
import GID_Create as GC

class Map:
    def __init__(self, mapsize):
        self.mapsize = mapsize
        Datum = GDFM.Create_FloorMap(mapsize)
        self.data = (Datum[0])
        self.PlayerLocation = Datum[3]
        self.ExitLocation = Datum[4]
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, mapsize, tileset):
        MapData = tp.initial(mapsize)
        self.width = MapData[1][1] * TILESIZE
        self.height = MapData[1][2] * TILESIZE
        self.tmdata = MapData
        self.player_location = MapData[1][4]
        self.original_map = MapData[1][0]
        self.tileset_location = tileset

    def render(self, surface):
        ti = GC.Tile_GID_Parser(self.tileset_location)
        for y in list(enumerate(self.tmdata[0])):
            for x in list(enumerate(y[1])):
                tile = ti[int(x[1])]
                surface.blit(tile, (x[0] * TILESIZE, y[0] * TILESIZE))
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        #scaled_surface = pg.Surface((self.width*2, self.height*2))
        #pg.transform.scale2x(temp_surface, scaled_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)

