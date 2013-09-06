# -*- coding: utf-8 -*-
import pygame

from loaders import *
from pygame.locals import *


class Ground(pygame.sprite.OrderedUpdates):
    def __init__(self, x, y, data, tile_w, tile_h, xy):
        super(Ground, self).__init__()
        self.data = data
        self.h_tiles, self.y_tiles = x, y
        self.tile_w, self.tile_h = tile_w, tile_h
        self.xy = xy

    def move(self, x, y):
        for tile in self:
            tile.rect.right += self.tile_w*x
            tile.rect.bottom += self.tile_h*y
        self.xy[0], self.xy[1] = self.xy[0]+x, self.xy[1]+y


class Tile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, x_co, y_co, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect(bottom=y_pos, right=x_pos)
        self.x_co, self.y_co = x_co, y_co

    def move(self, x, y):
        #print "before x: "+str(self.rect.right)+"\ty: "+str(self.rect.bottom)
        self.rect.right += 40*x
        self.rect.bottom += 26*y
        #print "after x: "+str(self.rect.right)+"\ty: "+str(self.rect.bottom)


class AnimatedTile(Tile):
    def __init__(self, x_pos, y_pos, x_co, y_co, images, fps=5):
        super(AnimatedTile, self).__init__(x_pos, y_pos, x_co, y_co, images[0])

        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0
        self.dir = 1

        # Call update to set our first image.
        self.update(pygame.time.get_ticks())

    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

        if t - self._last_update > self._delay:
            self._frame += self.dir
            if self._frame == 0:
                self.dir = 1
                self._frame += self.dir
            if self._frame >= len(self._images):
                self.dir = (-1)
                self._frame += self.dir
            self.image = self._images[self._frame]
            self._last_update = t


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)


class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, font, text, color=(180, 180, 180), center=False):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.cursor = load_image("sword.png", tp=True)
        w, h = self.font.size(text)
        c = 0
        if center:
            x = x-w/2
        else:
            x = x-self.cursor.get_width()
            c = self.cursor.get_width()
        self.rect = pygame.Rect(x-c, y-h, w+c, h)
        self.color = color
        self.text = text
        self.image = pygame.Surface(
            (self.rect.width, self.rect.height),
            pygame.SRCALPHA,
            32
        )
        self.image.convert_alpha()
        self.image.blit(self.font.render(self.text, True, self.color), (c, 0))
        self.last_update = 0

    def move(self, x, y):
        self.rect.left += x
        self.rect.top += y

    def delay(self, delay):
        t = pygame.time.get_ticks()
        if t - self.last_update > delay:
            self.last_update = t
            return t
        return False


class MenuItem(Text):
    def __init__(
        self, x, y, font, text, action,
        hovered=False,
        centering=False,
        color=(180, 180, 180),
        hovercolor=(250, 100, 25)
    ):
        super(MenuItem, self).__init__(x, y, font, text, color, centering)
        self.hovercolor = hovercolor
        self.hovered = hovered
        self.rect.width += self.cursor.get_width()
        if self.hovered:
            self.hover()
        self.action = action

    def hover(self):
        image = pygame.Surface(
            (self.rect.width, self.rect.height),
            pygame.SRCALPHA,
            32
        )
        image.convert_alpha()
        image.blit(
            self.cursor,
            (0, self.rect.height/2-self.cursor.get_height()/2)
        )
        image.blit(
            self.font.render(self.text, True, self.hovercolor),
            (self.cursor.get_width(), 0)
        )
        self.image = image
        self.hovered = True

    def normal(self):
        image = pygame.Surface(
            (self.rect.width, self.rect.height),
            pygame.SRCALPHA,
            32
        )
        image.convert_alpha()
        image.blit(
            self.font.render(self.text, True, self.color),
            (self.cursor.get_width(), 0)
        )
        self.image = image
        self.hovered = False


class MusicPlayer(object):

    def __init__(self, song=""):

        self.songend = pygame.USEREVENT + 1  # Whenever a track ends..
        self.tracknumber = 0
        if song:
            self.musiclist = [song]
        else:
            self.musiclist = load_files("music", ".ogg")   # another one
        load_music(self.musiclist[self.tracknumber])   # is loaded
        pygame.mixer.music.set_endevent(self.songend)  # and added
        if len(self.musiclist) > 1:
            self.tracknumber += 1                      # to the queue
        pygame.mixer.music.queue("music/"+self.musiclist[self.tracknumber])

    def next(self):
        if pygame.event.peek(self.songend):
            self.tracknumber += 1
            if self.tracknumber+1 >= len(self.musiclist):
                self.tracknumber = 0
                track = "music/"+self.musiclist[self.tracknumber]
                pygame.mixer.music.queue(track)
            else:
                track = "music/"+self.musiclist[self.tracknumber+1]
                pygame.mixer.music.queue(track)


class Mouse(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
