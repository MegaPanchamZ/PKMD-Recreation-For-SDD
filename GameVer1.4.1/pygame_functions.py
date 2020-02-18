# pg_functions

import pygame as pg
import math, sys, os

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()
pg.mixer.init()
spriteGroup = pg.sprite.OrderedUpdates()
textboxGroup = pg.sprite.OrderedUpdates()
gameClock = pg.time.Clock()
musicPaused = False
hiddenSprites = pg.sprite.OrderedUpdates()
screenRefresh = True
background = None

keydict = {"space": pg.K_SPACE, "esc": pg.K_ESCAPE, "up": pg.K_UP, "down": pg.K_DOWN,
           "left": pg.K_LEFT, "right": pg.K_RIGHT, "return": pg.K_RETURN,
           "a": pg.K_a,
           "b": pg.K_b,
           "c": pg.K_c,
           "d": pg.K_d,
           "e": pg.K_e,
           "f": pg.K_f,
           "g": pg.K_g,
           "h": pg.K_h,
           "i": pg.K_i,
           "j": pg.K_j,
           "k": pg.K_k,
           "l": pg.K_l,
           "m": pg.K_m,
           "n": pg.K_n,
           "o": pg.K_o,
           "p": pg.K_p,
           "q": pg.K_q,
           "r": pg.K_r,
           "s": pg.K_s,
           "t": pg.K_t,
           "u": pg.K_u,
           "v": pg.K_v,
           "w": pg.K_w,
           "x": pg.K_x,
           "y": pg.K_y,
           "z": pg.K_z,
           "1": pg.K_1,
           "2": pg.K_2,
           "3": pg.K_3,
           "4": pg.K_4,
           "5": pg.K_5,
           "6": pg.K_6,
           "7": pg.K_7,
           "8": pg.K_8,
           "9": pg.K_9,
           "0": pg.K_0}
screen = ""


class Background():
    def __init__(self):
        self.colour = pg.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def scroll(self, x, y):
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        screen.blit(self.tiles[row][col], [xOff, yOff])
        screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        self.surface = screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        screen.fill(self.colour)
        pg.display.update()
        self.surface = screen.copy()


class newSprite(pg.sprite.Sprite):
    def __init__(self, filename, frames=1):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)
        if screenRefresh:
            updateDisplay()


class newTextBox(pg.sprite.Sprite):
    def __init__(self, text, xpos, ypos, width, case, maxLength, fontSize):
        pg.sprite.Sprite.__init__(self)
        self.text = ""
        self.width = width
        self.initialText = text
        self.case = case
        self.maxLength = maxLength
        self.boxSize = int(fontSize * 1.7)
        self.image = pg.Surface((width, self.boxSize))
        self.image.fill((255, 255, 255))
        pg.draw.rect(self.image, (0, 0, 0), [0, 0, width - 1, self.boxSize - 1], 2)
        self.rect = self.image.get_rect()
        self.fontFace = pg.font.match_font("Arial")
        self.fontColour = pg.Color("black")
        self.initialColour = (180, 180, 180)
        self.font = pg.font.Font(self.fontFace, fontSize)
        self.rect.topleft = [xpos, ypos]
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])

    def update(self, keyevent):
        key = keyevent.key
        unicode = keyevent.unicode
        if key > 31 and key < 127 and (
                self.maxLength == 0 or len(self.text) < self.maxLength):  # only printable characters
            if keyevent.mod in (1, 2) and self.case == 1 and key >= 97 and key <= 122:
                # force lowercase letters
                self.text += chr(key)
            elif keyevent.mod == 0 and self.case == 2 and key >= 97 and key <= 122:
                self.text += chr(key - 32)
            else:
                # use the unicode char
                self.text += unicode

        elif key == 8:
            # backspace. repeat until clear
            keys = pg.key.get_pressed()
            nexttime = pg.time.get_ticks() + 200
            deleting = True
            while deleting:
                keys = pg.key.get_pressed()
                if keys[pg.K_BACKSPACE]:
                    thistime = pg.time.get_ticks()
                    if thistime > nexttime:
                        self.text = self.text[0:len(self.text) - 1]
                        self.image.fill((255, 255, 255))
                        pg.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
                        newSurface = self.font.render(self.text, True, self.fontColour)
                        self.image.blit(newSurface, [10, 5])
                        updateDisplay()
                        nexttime = thistime + 50
                        pg.event.clear()
                else:
                    deleting = False

        self.image.fill((255, 255, 255))
        pg.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.text, True, self.fontColour)
        self.image.blit(newSurface, [10, 5])
        if screenRefresh:
            updateDisplay()

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.topleft = [xpos, ypos]
        else:
            self.rect.center = [xpos, ypos]

    def clear(self):
        self.image.fill((255, 255, 255))
        pg.draw.rect(self.image, (0, 0, 0), [0, 0, self.width - 1, self.boxSize - 1], 2)
        newSurface = self.font.render(self.initialText, True, self.initialColour)
        self.image.blit(newSurface, [10, 5])
        if screenRefresh:
            updateDisplay()


class newLabel(pg.sprite.Sprite):
    def __init__(self, text, fontSize, font, fontColour, xpos, ypos, background):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.fontColour = parseColour(fontColour)
        self.fontFace = pg.font.match_font(font)
        self.fontSize = fontSize
        self.background = background
        self.font = pg.font.Font(self.fontFace, self.fontSize)
        self.renderText()
        self.rect.topleft = [xpos, ypos]

    def update(self, newText, fontColour, background):
        self.text = newText
        if fontColour:
            self.fontColour = parseColour(fontColour)
        if background:
            self.background = parseColour(background)

        oldTopLeft = self.rect.topleft
        self.renderText()
        self.rect.topleft = oldTopLeft
        if screenRefresh:
            updateDisplay()

    def renderText(self):
        lineSurfaces = []
        textLines = self.text.split("<br>")
        maxWidth = 0
        maxHeight = 0
        for line in textLines:
            lineSurfaces.append(self.font.render(line, True, self.fontColour))
            thisRect = lineSurfaces[-1].get_rect()
            if thisRect.width > maxWidth:
                maxWidth = thisRect.width
            if thisRect.height > maxHeight:
                maxHeight = thisRect.height
        self.image = pg.Surface((maxWidth, (self.fontSize + 1) * len(textLines) + 5), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        if self.background != "clear":
            self.image.fill(parseColour(self.background))
        linePos = 0
        for lineSurface in lineSurfaces:
            self.image.blit(lineSurface, [0, linePos])
            linePos += self.fontSize + 1
        self.rect = self.image.get_rect()


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pg.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (xpos, ypos + 50)
    else:
        windowInfo = pg.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitorWidth - sizex) / 2, (monitorHeight - sizey) / 2)
    if fullscreen:
        screen = pg.display.set_mode([sizex, sizey], pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode([sizex, sizey])
    background = Background()
    screen.fill(background.colour)
    pg.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pg.display.update()
    return screen


def moveSprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screenRefresh:
        updateDisplay()


def rotateSprite(sprite, angle):
    print("rotateSprite has been deprecated. Please use transformSprite")
    transformSprite(sprite, angle, 1)


def transformSprite(sprite, angle, scale, hflip=False, vflip=False):
    oldmiddle = sprite.rect.center
    if hflip or vflip:
        tempImage = pg.transform.flip(sprite.images[sprite.currentImage], hflip, vflip)
    else:
        tempImage = sprite.images[sprite.currentImage]
    if angle != 0 or scale != 1:
        sprite.angle = angle
        sprite.scale = scale
        tempImage = pg.transform.rotozoom(tempImage, -angle, scale)
    sprite.image = tempImage
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = oldmiddle
    sprite.mask = pg.mask.from_surface(sprite.image)
    if screenRefresh:
        updateDisplay()


def killSprite(sprite):
    sprite.kill()
    if screenRefresh:
        updateDisplay()


def setBackgroundColour(colour):
    background.setColour(colour)
    if screenRefresh:
        updateDisplay()


def setBackgroundImage(img):
    global background
    background.setTiles(img)
    if screenRefresh:
        updateDisplay()


def hideSprite(sprite):
    hiddenSprites.add(sprite)
    spriteGroup.remove(sprite)
    if screenRefresh:
        updateDisplay()


def hideAll():
    hiddenSprites.add(spriteGroup.sprites())
    spriteGroup.empty()
    if screenRefresh:
        updateDisplay()


def unhideAll():
    spriteGroup.add(hiddenSprites.sprites())
    hiddenSprites.empty()
    if screenRefresh:
        updateDisplay()


def showSprite(sprite):
    spriteGroup.add(sprite)
    if screenRefresh:
        updateDisplay()


def makeSprite(filename, frames=1):
    thisSprite = newSprite(filename, frames)
    return thisSprite


def addSpriteImage(sprite, image):
    sprite.addImage(image)


def changeSpriteImage(sprite, index):
    sprite.changeImage(index)


def nextSpriteImage(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)


def prevSpriteImage(sprite):
    sprite.currentImage -= 1
    if sprite.currentImage < 0:
        sprite.currentImage = len(sprite.images) - 1
    sprite.changeImage(sprite.currentImage)


def makeImage(filename):
    return loadImage(filename)


def touching(sprite1, sprite2):
    collided = pg.sprite.collide_mask(sprite1, sprite2)
    return collided


def allTouching(spritename):
    if spriteGroup.has(spritename):
        collisions = pg.sprite.spritecollide(spritename, spriteGroup, False, collided=pg.sprite.collide_mask)
        collisions.remove(spritename)
        return collisions
    else:
        return []


def pause(milliseconds, allowEsc=True):
    keys = pg.key.get_pressed()
    current_time = pg.time.get_ticks()
    waittime = current_time + milliseconds
    updateDisplay()
    while not (current_time > waittime or (keys[pg.K_ESCAPE] and allowEsc)):
        pg.event.clear()
        keys = pg.key.get_pressed()
        if (keys[pg.K_ESCAPE] and allowEsc):
            pg.quit()
            sys.exit()
        current_time = pg.time.get_ticks()


def drawRect(xpos, ypos, width, height, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pg.draw.rect(screen, colour, [xpos, ypos, width, height], linewidth)
    if screenRefresh:
        pg.display.update(thisrect)


def drawLine(x1, y1, x2, y2, colour, linewidth=1):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pg.draw.line(screen, colour, (x1, y1), (x2, y2), linewidth)
    if screenRefresh:
        pg.display.update(thisrect)


def drawPolygon(pointlist, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pg.draw.polygon(screen, colour, pointlist, linewidth)
    if screenRefresh:
        pg.display.update(thisrect)


def drawEllipse(centreX, centreY, width, height, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pg.Rect(centreX - width / 2, centreY - height / 2, width, height)
    pg.draw.ellipse(screen, colour, thisrect, linewidth)
    if screenRefresh:
        pg.display.update(thisrect)


def drawTriangle(x1, y1, x2, y2, x3, y3, colour, linewidth=0):
    global bgSurface
    colour = parseColour(colour)
    thisrect = pg.draw.polygon(screen, colour, [(x1, y1), (x2, y2), (x3, y3)], linewidth)
    if screenRefresh:
        pg.display.update(thisrect)


def clearShapes():
    global background
    screen.blit(background.surface, [0, 0])
    if screenRefresh:
        updateDisplay()


def updateShapes():
    pg.display.update()


def end():
    pg.quit()


def makeSound(filename):
    pg.mixer.init()
    thissound = pg.mixer.Sound(filename)

    return thissound


def playSound(sound, loops=0):
    sound.play(loops)


def stopSound(sound):
    sound.stop()


def playSoundAndWait(sound):
    sound.play()
    while pg.mixer.get_busy():
        # pause
        pause(10)


def makeMusic(filename):
    pg.mixer.music.load(filename)


def playMusic(loops=0):
    global musicPaused
    if musicPaused:
        pg.mixer.music.unpause()
    else:
        pg.mixer.music.play(loops)
    musicPaused = False


def stopMusic():
    pg.mixer.music.stop()


def pauseMusic():
    global musicPaused
    pg.mixer.music.pause()
    musicPaused = True


def rewindMusic():
    pg.mixer.music.rewind()


def endWait():
    updateDisplay()
    print("Press ESC to quit")
    keys = pg.key.get_pressed()
    current_time = pg.time.get_ticks()
    waittime = 0
    while not keys[pg.K_ESCAPE]:
        current_time = pg.time.get_ticks()
        if current_time > waittime:
            pg.event.clear()
            keys = pg.key.get_pressed()
            waittime += 20
    pg.quit()


def keyPressed(keyCheck=""):
    global keydict
    pg.event.clear()
    keys = pg.key.get_pressed()
    if sum(keys) > 0:
        if keyCheck == "" or keys[keydict[keyCheck.lower()]]:
            return True
    return False


def makeLabel(text, fontSize, xpos, ypos, fontColour='black', font='Arial', background="clear"):
    # make a text sprite
    thisText = newLabel(text, fontSize, font, fontColour, xpos, ypos, background)
    return thisText


def moveLabel(sprite, x, y):
    sprite.rect.topleft = [x, y]
    if screenRefresh:
        updateDisplay()


def changeLabel(textObject, newText, fontColour=None, background=None):
    textObject.update(newText, fontColour, background)
    # updateDisplay()


def waitPress():
    pg.event.clear()
    keypressed = False
    thisevent = pg.event.wait()
    while thisevent.type != pg.KEYDOWN:
        thisevent = pg.event.wait()
    return thisevent.key


def makeTextBox(xpos, ypos, width, case=0, startingText="Please type here", maxLength=0, fontSize=22):
    thisTextBox = newTextBox(startingText, xpos, ypos, width, case, maxLength, fontSize)
    textboxGroup.add(thisTextBox)
    return thisTextBox


def textBoxInput(textbox, functionToCall=None, args=[]):
    # starts grabbing key inputs, putting into textbox until enter pressed
    global keydict
    textbox.text = ""
    returnVal = None
    while True:
        updateDisplay()
        if functionToCall:
            returnVal = functionToCall(*args)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    textbox.clear()
                    if returnVal:
                        return textbox.text, returnVal
                    else:
                        return textbox.text
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                else:
                    textbox.update(event)
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()


def clock():
    current_time = pg.time.get_ticks()
    return current_time


def tick(fps):
    pg.event.clear()
    keys = pg.key.get_pressed()
    if (keys[pg.K_ESCAPE]):
        pg.quit()
        sys.exit()
    gameClock.tick(fps)
    return gameClock.get_fps()


def showLabel(labelName):
    textboxGroup.add(labelName)
    if screenRefresh:
        updateDisplay()


def hideLabel(labelName):
    textboxGroup.remove(labelName)
    if screenRefresh:
        updateDisplay()


def showTextBox(textBoxName):
    textboxGroup.add(textBoxName)
    if screenRefresh:
        updateDisplay()


def hideTextBox(textBoxName):
    textboxGroup.remove(textBoxName)
    if screenRefresh:
        updateDisplay()


def updateDisplay():
    global background
    spriteRects = spriteGroup.draw(screen)
    textboxRects = textboxGroup.draw(screen)
    pg.display.update()
    keys = pg.key.get_pressed()
    if (keys[pg.K_ESCAPE]):
        pg.quit()
        sys.exit()
    spriteGroup.clear(screen, background.surface)
    textboxGroup.clear(screen, background.surface)


def mousePressed():
    pg.event.clear()
    mouseState = pg.mouse.get_pressed()
    if mouseState[0]:
        return True
    else:
        return False


def spriteClicked(sprite):
    mouseState = pg.mouse.get_pressed()
    if not mouseState[0]:
        return False  # not pressed
    pos = pg.mouse.get_pos()
    if sprite.rect.collidepoint(pos):
        return True
    else:
        return False


def parseColour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pg.Color(colour)
    else:
        colourRGB = pg.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]
        return colourRGB


def mouseX():
    x = pg.mouse.get_pos()
    return x[0]


def mouseY():
    y = pg.mouse.get_pos()
    return y[1]


def scrollBackground(x, y):
    global background
    background.scroll(x, y)


def setAutoUpdate(val):
    global screenRefresh
    screenRefresh = val

