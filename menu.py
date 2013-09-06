# -*- coding: utf-8 -*-
import pygame
from classes import *
from game import *


class Menu(object):
    def __init__(self, screen, movekeys):
        self.width, self.height = screen.get_width(), screen.get_height()
        self.font = pygame.font.Font('fonts/Morpheus.ttf', 36)
        self.screen = screen

        self.movekeys = movekeys

        self.menu = pygame.sprite.OrderedUpdates()
        self.state = 0

        self.background = pygame.Surface((self.width, self.height))
        self.texture = load_image("menutext.png")
        i = 0
        while i < self.width:
            j = 0
            while j < self.height:
                self.background.blit(self.texture, (i, j))
                j += 300
            i += 300

        self.musicplayer = MusicPlayer("menu.ogg")
        self.background = self.background.convert()
        self.titletext = pygame.sprite.GroupSingle()
        self.titletext.add(Text(
            self.width/2,                # x position
            0,                      # y position
            self.font,              # font object
            "Isometric",                  # text string
            center=True             # center text or not
        ))

    def main(self):
        pygame.mixer.music.play()           # Start playing music

        while True:
            self.musicplayer.next()         # See if playback is finished
            self.input()                    # Get user input.
            if self.state == 0:
                self.intro()
            self.draw()                     # Draw sprites
            pygame.time.Clock().tick(60)   # Sets the fps of the game
            if self.state == 2:
                return "game"

    def intro(self):
        t = self.titletext.sprite.delay(1000/60)
        if t:
            rect = self.titletext.sprite.rect
            title_pos = rect.height-rect.height-rect.height/4
            if self.titletext.sprite.rect.top < self.height/2-(title_pos):
                self.titletext.sprite.move(0, 1)

    def start_game(self):
        self.menu.empty()
        self.titletext.empty()
        self.state = 2

    def exit_game(self):
        exit()

    def options_menu(self):
        self.menu.empty()
        self.menu.add(MenuItem(
            self.width/2, 130,       # x & y positions
            self.font,          # font object
            "Back",             # button text
            "main_menu",        # button target
            hovered=True        # button is initially in hovered state
        ))

    def main_menu(self):
        self.menu.empty()
        self.titletext.add(Text(
            self.width/2, 65,        # x & y positions
            self.font,          # font object
            "Isometric",              # text string
            (190, 190, 190),    # text colour
            center=True         # if text is centered
        ))
        self.menu.add(MenuItem(
            self.width/2, 130,       # x & y positions
            self.font,          # font object
            "Start",            # button text
            "start_game",       # button target
            hovered=True        # button is initially in hovered state
        ))
        self.menu.add(MenuItem(
            self.width/2, 195,       # x & y positions
            self.font,          # font object
            "Options",          # button text
            "options_menu"      # button target
        ))
        self.menu.add(MenuItem(
            self.width/2, 260,       # x & y positions
            self.font,          # font object
            "Exit",             # button text
            "exit_game"         # button target
        ))

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
            elif key in self.movekeys.keys():
                menulist = []
                for button in self.menu:
                    menulist.append(button)  # Buttons
                if len(menulist) > 1:
                    next = self.movekeys[key][1]  # Get direction
                    for i, button in enumerate(menulist):
                        if button.hovered:
                            if (i-next) < 0:  # From top to bottom
                                next = (len(menulist)-1)
                            elif (i-next) > (len(menulist)-1):  # Bottom to top
                                next = 0
                            else:
                                next = i-next
                            menulist[i].normal()  # Un-hover current button
                    menulist[next].hover()  # Hover next button

    def perform_action(self, name):
        function = getattr(self, name)
        function()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.titletext.draw(self.screen)
        self.menu.draw(self.screen)
        pygame.display.update()

    def input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:  # one way of getting keyboard presses
                self.key_action(event.key)
