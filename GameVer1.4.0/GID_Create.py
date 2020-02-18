
import pygame
import pygame.locals

def load_tile_table(filename, width, height):
    image = pygame.image.load(filename)
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_y in range(0, int(image_height/height) -1):
        #line = []
        #tile_table.append(line)
        for tile_x in range(0, int(image_width/width) -1):
            if tile_x == 0:
                if tile_y == 0:
                    rect = (tile_x * width + 1, tile_y * height + 1, width, height)
                    #line.append(image.subsurface(rect))
                    tile_table.append(image.subsurface(rect))
                else:
                    rect = (tile_x * width + 1, tile_y * height + tile_y + 1 , width, height)
                    #line.append(image.subsurface(rect))
                    tile_table.append(image.subsurface(rect))
            else:
                rect = (tile_x * width + tile_x + 1, tile_y * height + tile_y + 1, width, height)
                #line.append(image.subsurface(rect))
                tile_table.append(image.subsurface(rect))

    return tile_table

def Tile_GID_Parser(file_path):
    table = load_tile_table(file_path, 24, 24)
    return table

'''
pygame.init()
screen = pygame.display.set_mode((128, 98))
screen.fill((255, 255, 255))
table = Tile_GID_Parser('Brine Cave.png')
screen.blit(table[4], (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.locals.QUIT:
    pass
'''

'''
if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((750, 650))
    screen.fill((255, 255, 255))
    table = load_tile_table("Brine Cave.png", 24, 24)
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*24, y*24))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
'''