# -*- coding: utf-8 -*-
import pygame
import json
from classes import *
from loaders import *

TILE_W, TILE_H = 40, 26


class Game(object):
    def __init__(self, screen, movekeys):
        self.movekeys = movekeys
        self.screen = screen
        self.width, self.height = screen.get_width(), screen.get_height()
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))
        self.emptytile = load_image("white.png", tp=True)
        self.emptytile.convert_alpha()
        self.musicplayer = MusicPlayer()
        self.mouse = Mouse(pygame.Rect(0, 0, 1, 1))
        self.player = pygame.sprite.GroupSingle()
        with open('maps/test.json') as data_file:
            self.data = json.load(data_file)
        self.animated = [0, 0, 1, 0, 0]
        self.centerx, self.centery = 0, 0
        self.texture = load_sliced_sprites(
            TILE_W+12,             # width
            TILE_H,                # height
            self.data["texture"],  # texture file
            self.animated          # list of animated sprites
        )  # load textures

    """ main function """
    def main(self):
        pygame.mixer.music.play()           # Start playing music
        self.draw_map2((9, 9))
        while True:
            self.musicplayer.next()         # See if playback is finished
            self.input()                    # Get user input.
            try:
                self.ground.update(pygame.time.get_ticks())
            except:
                pass
            self.draw()                     # Draw sprites
            pygame.time.Clock().tick(60)   # Sets the fps of the game

    def draw_map2(self, move):

        self.centerx += move[0]  # x-position of player (center of the screen)
        self.centery += move[1]  # y-position of player (center of the screen)
        rows = self.data["rows"]
        texture = self.texture
        textmap = []
        tilemap = []

        horizontal_tiles = self.width/TILE_W         # amount of x tiles to draw
        vertical_tiles = (self.width/TILE_H+2)/2    # amount of y tiles to draw
        xy = [self.centerx, self.centery]
        self.ground = Ground(horizontal_tiles, vertical_tiles, rows, TILE_W, TILE_H, xy)
        x, y = 0, vertical_tiles*2              # iterators for dicts

        for i in xrange(
            self.centery+vertical_tiles,        # bottom border
            self.centery-vertical_tiles,        # top border
            -1                                  # reversed direction
        ):
            line = ""
            row = []
            tileID = []
            for j in xrange(
                self.centerx - horizontal_tiles,  # left border
                self.centerx + horizontal_tiles   # right border
            ):
                vert = (vertical_tiles*2-y)*13      # vertical offset
                hori = horizontal_tiles/4 * TILE_W  # horizontal offset
                x_pos = x * TILE_W - vert - hori
                y_pos = self.width-(y - 1)*TILE_H

                image = self.emptytile  # empty tile if no tile found
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
                        iddd = (i, j)

                tileID.append(iddd)

                if i == self.centery and j == self.centerx:
                    image = texture[0]
                    im = 0
                    item = "P"

                line += str(item)
                if im >= 0:
                    if self.animated[im]:
                        self.ground.add(AnimatedTile(
                            x_pos,
                            y_pos,
                            i, j,
                            image
                        ))
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

    def draw_map(self, move):

        self.centerx += move[0]  # x-position of player (center of the screen)
        self.centery += move[1]  # y-position of player (center of the screen)
        rows = self.data["rows"]
        texture = self.texture
        textmap = []
        tilemap = []

        horizontal_tiles = self.width/TILE_W         # amount of x tiles to draw
        vertical_tiles = (self.width/TILE_H+2)/2    # amount of y tiles to draw
        self.ground = Ground(horizontal_tiles, vertical_tiles, self.data, TILE_W, TILE_H)
        x, y = 0, vertical_tiles*2              # iterators for dicts

        for i in xrange(
            self.centery+vertical_tiles,        # bottom border
            self.centery-vertical_tiles,        # top border
            -1                                  # reversed direction
        ):
            line = ""
            row = []
            tileID = []
            for j in xrange(
                self.centerx - horizontal_tiles,  # left border
                self.centerx + horizontal_tiles   # right border
            ):
                vert = (vertical_tiles*2-y)*13      # vertical offset
                hori = horizontal_tiles/4 * TILE_W  # horizontal offset
                x_pos = x * TILE_W - vert - hori
                y_pos = self.width-(y - 1)*TILE_H

                image = self.emptytile  # empty tile if no tile found
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
                        iddd = (i, j)

                tileID.append(iddd)

                if i == self.centery and j == self.centerx:
                    image = texture[0]
                    im = 0
                    item = "P"

                line += str(item)
                if im >= 0:
                    if self.animated[im]:
                        self.ground.add(AnimatedTile(
                            x_pos,
                            y_pos,
                            i, j,
                            image
                        ))
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

    def input(self):
        self.mouse.rect.center = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

                # get keyboard presses, better for multiple keys at once
                pressed_keys = pygame.key.get_pressed()
                x, y = 0, 0
                for key, value in self.movekeys.items():
                    if pressed_keys[key]:
                        x += value[0]
                        y += value[1]

                if x != 0 or y != 0:
                    self.ground.move(x, y)

            if event.type == USEREVENT+1:  # use this to catch timers
                pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ground.draw(self.screen)
        pygame.display.update()
