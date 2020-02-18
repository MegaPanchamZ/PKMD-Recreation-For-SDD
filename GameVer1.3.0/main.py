
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from TileMap import *

playerlocale = "placeholder"


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        mapname = 'Crystal Cave Lower' + '.png'
        tileset = game_folder + '/Assets/Tiles_Appropriated/ready/' + mapname
        self.map = TiledMap('M', tileset)
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        '''
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '#':
                    Wall(self, col, row)
        '''
        self.player = Player(self, self.map.player_location[0], self.map.player_location[1])
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)

                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)

                if event.key == pg.K_UP:
                    self.player.move(dy=-1)

                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)



    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

# create the game object

def GameBegin():
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()

GameBegin()
