# -*- coding: utf-8 -*-
import os
import pygame

from menu import *
from loaders import *
from classes import *
from pygame.locals import *

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'
    
COLOURS = {
    'white': (255, 255, 255),
    'text': (190, 190, 190),
    'hover': (250, 100, 25)
}


class MainGame(object):         # Game class

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # sounds
        pygame.init()
        pygame.display.set_caption("Isometric2")  # Set app name
        pygame.key.set_repeat(500, 100)

        self.movekeys = {
            97:  (1, 0),     # a
            100: (-1, 0),    # d
            115: (0, -1),    # s
            119: (0, 1),     # w
            273: (0, 1),     # up
            274: (0, -1),    # down
            275: (-1, 0),     # right
            276: (1, 0)     # left
        }

        info = pygame.display.Info()  # get display info
        xpos = info.current_w/2-800/2  # get screen width
        ypos = info.current_h/2-600/2  # get screen height
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xpos, ypos)  # center

        self.width, self.height = 800, 600

        self.screen = pygame.display.set_mode((self.width, self.height))

    """ main function """
    def main(self):
        self.menu = Menu(self.screen, self.movekeys)
        while True:
            if self.menu.main() == "game":
                self.game = Game(self.screen, self.movekeys)
                self.game.main()


if __name__ == '__main__':
    game = MainGame()
    game.main()
