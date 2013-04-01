# -*- coding: utf-8 -*-
import os
import pygame
import random
import json

from loaders import *
from classes import *
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

WIDTH, HEIGHT = 1920, 1080
DELAY     = 500             #Delay when pressing keys
INTERVAL  = 100
FPS = 60 #change according to what the game needs. 60 is a common hz for screens
SIZE = WIDTH, HEIGHT #Screen size
TITLE = 'Isometric'      #Game window title
FONT = 'morpheus.ttf', 60
TILE_W, TILE_H = 40, 26

COLOURS = {
    'white': (255, 255, 255),
    'text': (190, 190, 190),
    'hover': (250, 100, 25)
}

"""Audio settings"""
FREQUENCY = 44100           #Audio CD quality
BITSIZE   = -16             #Unsigned 16 bit
CHANNEL   = 2               #1 is mono, 2 is stereo
BUFFER    = 2048            #Number of samples (experiment to get right sound)

""" Game class """
class Game(object):

    def __init__(self):

        pygame.mixer.pre_init(FREQUENCY, BITSIZE, CHANNEL, BUFFER)  # pre_init makes sounds work
        pygame.init()
        pygame.display.set_caption(TITLE)                           # Set app name
        pygame.key.set_repeat(DELAY, INTERVAL)                      #

        info = pygame.display.Info()                                # This block of code
        xpos = info.current_w/2-WIDTH/2                             # positions the application
        ypos = info.current_h/2-HEIGHT/2                            # to the middle of the current
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xpos, ypos) # screen when initialized.

        self.screen = pygame.display.set_mode((SIZE))               # Set screen size


        self.movekeys = {
            97:(1, 0),     # a
            100:(-1, 0),     # d
            115:(0, -1),     # s
            119:(0, 1),    # w
            273:(0, 1),     # up
            274:(0, -1),    # down
            275:(1, 0),     # right
            276:(-1, 0)     # left
        }

        self.font = pygame.font.Font('fonts/'+FONT[0], FONT[1])
        self.state = 0
        self.menu = pygame.sprite.OrderedUpdates()
        self.ground = pygame.sprite.OrderedUpdates()

        self.centerx, self.centery = 0, 0

        with open('maps/test2.json') as data_file:    
            self.data = json.load(data_file)
        self.animated = [0, 0, 1, 0, 0]
        self.texture = load_sliced_sprites(TILE_W+12, TILE_H, self.data["texture"], self.animated) #load textures'
        
        print self.texture

        self.background = pygame.Surface(SIZE)
        self.background.fill(COLOURS['white'])
        self.background = self.background.convert()

        self.emptytile = load_image("white.png", tp=True)
        self.emptytile.convert_alpha()

        self.mouse = Mouse(pygame.Rect(0, 0, 1, 1))
        self.musicplayer = MusicPlayer()
        self.player = pygame.sprite.GroupSingle()
        self.titletext = pygame.sprite.GroupSingle()
        self.titletext.add(Text( WIDTH/2, 0, self.font, TITLE, centering=True) ) 
        pygame.display.flip()

    """ main function """
    def main(self):
        pygame.mixer.music.play()           #Start playing music
        

        #self.player.add(Player(pygame.Rect(), ""))

        while True:
            self.musicplayer.next()         #See if playback is finished or not
            self.input()                    #Get user input. Mouse clicks, movements and keyboard presses.
            self.logic()
            self.ground.update(pygame.time.get_ticks())
            self.draw()                     #Draw sprites
            pygame.time.Clock().tick(FPS)   #Sets the fps of the game

    def logic(self):
        """game logic"""

        #intro animation
        if self.state == 0:
            t = self.titletext.sprite.delay(1000/FPS)
            if t:
                if self.titletext.sprite.rect.top < HEIGHT/2-(self.titletext.sprite.rect.height-self.titletext.sprite.rect.height/4):
                    self.titletext.sprite.move(0, 1)

    #"texture": 2 def draw_rest(self, move):


    def draw_map(self, move):
        self.centerx += move[0] #x-position of player (center of the screen)
        self.centery += move[1] #y-position of player (center of the screen)
        rows = self.data["rows"]
        texture = self.texture
        self.ground.empty()
        textmap = []
        tilemap = []

        horizontal_tiles = WIDTH/TILE_W         #calculate amount of horizontal tiles to draw
        vertical_tiles = (HEIGHT/TILE_H+2)/2    #calculate amount of vertical tiles to draw
        x, y = 0, vertical_tiles*2              #iterators for the dictionaries

        for i in xrange(self.centery+vertical_tiles, self.centery-vertical_tiles, -1):
            line = ""
            row = []
            tileID = []
            for j in xrange( self.centerx - horizontal_tiles, self.centerx + horizontal_tiles ):
                x_pos = x * TILE_W - ( vertical_tiles*2-y )*13 - ( horizontal_tiles/4 * TILE_W )
                y_pos = HEIGHT-( y - 1 )*TILE_H

                image = self.emptytile
                item = "."
                im = -1
                iddd = None

                if 0 <= i and i < len(rows):
                    if 0 <= j and j < len(rows[i]["tiles"]):
                        if "texture" in rows[i]["tiles"][j]:
                            item = rows[i]["tiles"][j]["texture"]
                            image = texture[item]
                            im = item

                        else:
                            item = rows[i]["default_texture"]
                            im = item
                            image = texture[item]
                        iddd = (i,j)

                tileID.append(iddd)

                if i == self.centery and j == self.centerx: 
                    #print j, i, self.centerx, self.centery
                    image = texture[0]
                    im = 0
                    item = "P"

                line += str(item)
                if im >= 0:
                    if self.animated[im]:
                        self.ground.add(AnimatedTile(x_pos, y_pos, i, j, image))
                    else:
                        self.ground.add(Tile(x_pos, y_pos, i, j, image))
                else:
                    self.ground.add(Tile(x_pos, y_pos, i, j, image))
                x += 1
                row.append((x_pos, y_pos))
            textmap.append(str(line))
            tilemap.append(tileID)
            x = 0
            y -= 1
        #for line in tilemap:
        #    print line

        """
        for row in data["rows"]:
            for tile in row["tiles"]:
                w = TILE_W-12
                x = 0 + tile["id"]*w+row["id"]*13
                y = HEIGHT-row["id"]*TILE_H
                print x, y
                try:texture
                    tex = tile["texture"]
                except:
                    tex = row["default_texture"]
                image = texture[tex]
                self.ground.add(Tile(x, y, image))
        """
    def start_game(self):
        self.menu.empty()
        self.titletext.empty()
        self.draw_map((9, 9))

    def perform_action(self, name):
        function = getattr(self, name)
        function()

    def exit_game(self):
        exit()

    def options_menu(self):
        self.menu.empty()
        self.menu.add(MenuItem( WIDTH/2, 130, self.font, "Back", "main_menu", hovered=True ))

    def main_menu(self):
        self.menu.empty()
        self.titletext.add(Text( WIDTH/2, 65, self.font, TITLE, COLOURS['text'], centering=True))
        self.menu.add(MenuItem( WIDTH/2, 130, self.font, "Start", "start_game", hovered=True ))
        self.menu.add(MenuItem( WIDTH/2, 195, self.font, "Options", "options_menu" ))
        self.menu.add(MenuItem( WIDTH/2, 260, self.font, "Exit", "exit_game" ))

    def key_action(self, key):
        if self.state == 0:
            if key:
                self.state = 1
                self.titletext.empty()
                self.main_menu()
        elif self.state == 1:
            if key == K_RETURN:
                for button in self.menu:
                    if button.hovered:
                        self.perform_action(button.action)
                        if button.text == "Start":
                            self.state = 2
            elif key in self.movekeys.keys():
                menulist = []
                for button in self.menu:
                    menulist.append(button.hovered)
                if len(menulist) > 1:
                    for i, val in enumerate(menulist):
                        if val == True:
                            menulist[i] = False
                            if i-self.movekeys[key][1] > len(menulist)-1:
                                menulist[0] = True
                            else:
                                menulist[i-self.movekeys[key][1]] = True
                            break
                    for i, button in enumerate(self.menu):
                        if menulist[i]: button.hover()
                        elif button.hovered: button.normal()

    def input(self):
        self.mouse.rect.center = pygame.mouse.get_pos()

        collisions = pygame.sprite.spritecollide(self.mouse, self.menu, 0)

        for event in pygame.event.get():

            # get keyboard presses, better for multiple keys at once
            pressed_keys = pygame.key.get_pressed()


            if event.type == QUIT: 
                exit()

            #if event.type == MOUSEBUTTONDOWN: #get mouse clicks 


            if self.state > 1:
                x, y = 0, 0
                for key, value in self.movekeys.items():
                    if pressed_keys[key]:
                        x += value[0]
                        y += value[1]

                if x != 0 or y != 0:
                    for tile in self.ground:
                        tile.move(x, y)

            if event.type == KEYDOWN: #one way of getting keyboard presses
                self.key_action(event.key)

            if event.type == USEREVENT+1: #use this to catch timers
                pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ground.draw(self.screen)
        self.titletext.draw(self.screen)
        self.menu.draw(self.screen)
        pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.main()