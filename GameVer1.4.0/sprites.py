import pygame as pg
from settings import *
import xml.etree.ElementTree as ET


class SpriteSheet:
    # load an atlas image
    def __init__(self, img_file, data_file=None):
        self.spritesheet = pg.image.load(img_file)
        self.map = {}
        if data_file:
            tree = ET.parse(data_file)
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('width'))
                    self.map[name]['height'] = int(node.attrib.get('height'))
        print(self.map)
    def get_image_rect(self, x, y, w, h):
        return self.spritesheet.subsurface(pg.Rect(x, y, w, h))

    def get_image_name(self, name):
        rect = pg.Rect(self.map[name]['x'], self.map[name]['y'],
                       self.map[name]['width'], self.map[name]['height'])
        return self.spritesheet.subsurface(rect)

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = pg.Rect(0,0,24,24)
        self.x = x
        self.y = y

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image_name("Idle-Down-1.png"),
                                self.game.spritesheet.get_image_name("Idle-Down-2.png"),
                                self.game.spritesheet.get_image_name("Idle-Down-3.png"),
                                self.game.spritesheet.get_image_name("Idle-Down-4.png"),
                                self.game.spritesheet.get_image_name("Idle-Down-5.png"),
                                self.game.spritesheet.get_image_name("Idle-Down-6.png"),
                                self.game.spritesheet.get_image_name("Idle-Down-7.png")]
        for frame in self.standing_frames:
            frame.set_colorkey(MAGENTA)
        self.walk_frames_r = [self.game.spritesheet.get_image_name("Walk-Right-1.png"),
                              self.game.spritesheet.get_image_name("Walk-Right-1.png"),
                              self.game.spritesheet.get_image_name("Walk-Right-1.png"),
                              self.game.spritesheet.get_image_name("Walk-Right-1.png")]
        for frame in self.walk_frames_r:
            frame.set_colorkey(MAGENTA)
        self.walk_frames_l = [self.game.spritesheet.get_image_name("Walk-Left-1.png"),
                              self.game.spritesheet.get_image_name("Walk-Left-2.png"),
                              self.game.spritesheet.get_image_name("Walk-Left-3.png"),
                              self.game.spritesheet.get_image_name("Walk-Left-4.png")]
        for frame in self.walk_frames_l:
            frame.set_colorkey(MAGENTA)


    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.animate()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def animate(self):
        now = pg.time.get_ticks()
        print(now)
        if self.game.events() == 'R':
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.walk_frames_r[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.game.events() == 'I':
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.w = 24
        self.h = 24
        self.rect = pg.Rect(x, y, self.w, self.h)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y