import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from TileMap import *
from random import choice, randint


class Game:
    def __init__(self, dungeon_size):
        pg.init()
        # Added pg.FULLSCREEN for fullscreen drawing, upscaled
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.dungeon_size = dungeon_size
        self.ai_move = False
        self.playerID = '25'
        self.enemy_1ID = '41'
        if dungeon_size =='S':
            self.mobcap = 10
        elif dungeon_size =='MS':
            self.mobcap = 15
        elif dungeon_size =='M':
            self.mobcap = 20
        elif dungeon_size =='ML':
            self.mobcap = 25
        elif dungeon_size =='L':
            self.mobcap = 25
        elif dungeon_size =='H':
            self.mobcap = 30
        elif dungeon_size =='G':
            self.mobcap = 40
        elif dungeon_size =='E':
            self.mobcap = 50

        self.mobcount = 0
        self.load_data()
        self.spawned = []
        self.moved = False

    def load_data(self):
        game_folder = path.dirname(__file__)
        mapname = 'Amp Plains' + '.png'
        tileset = game_folder + '/Assets/Tiles_Appropriated/ready/' + mapname
        Sprite_Folder = game_folder + '/Assets/Sprite/'
        self.map = TiledMap(self.dungeon_size, tileset)
        self.map_image = self.map.make_map()
        self.rooms = self.map.rooms
        self.map_rect = self.map_image.get_rect()

        self.spritesheet_player = SpriteSheet(Sprite_Folder + 'Sprite' +
                                              self.playerID + '/' + 'sprites.png', Sprite_Folder + 'Sprite' +
                                              self.playerID + '/' + 'sprites.xml')

        self.spritesheet_enemy_1 = SpriteSheet(Sprite_Folder + 'Sprite' +
                                               self.enemy_1ID + '/' + 'sprites.png', Sprite_Folder + 'Sprite' +
                                               self.enemy_1ID + '/' + 'sprites.xml')

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.original_map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)

        self.player = Player(self, self.map.player_location[0], self.map.player_location[1])
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            if self.ai_move:
                if self.mobcount < self.mobcap:
                    room_choice = choice(self.rooms)
                    location_choice = randint(room_choice[0] + 1, room_choice[0] + room_choice[2] - 1),\
                                      randint(room_choice[1] + 1, room_choice[1] + room_choice[3] - 1)
                    if location_choice not in self.spawned:
                        self.enemy = Enemy(self, location_choice[0], location_choice[1])
                        self.spawned.append(location_choice)
                        self.mobcount +=1

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
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        self.state = str('I')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                    self.state = 'L'
                    self.player.walking = True
                    self.player.last_dir = 'L'
                    self.ai_move = True
                    # self.moved = True
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                    self.state = 'R'
                    self.player.walking = True
                    self.player.last_dir = 'R'
                    self.ai_move = True
                    # self.moved = True
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                    self.state = 'U'
                    self.player.walking = True
                    self.player.last_dir = 'U'
                    self.ai_move = True
                    # self.moved = True
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                    self.state = 'D'
                    self.player.walking = True
                    self.player.last_dir = 'D'
                    self.ai_move = True
                    # self.moved = True
            else:
                # after 500 milliseconds do:
                self.state = 'I'
                self.player.walking = False
                self.idle = True
                self.ai_move = False
                # self.moved = False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object

def GameBegin(Size):
    g = Game(Size)
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()


GameBegin("G")
