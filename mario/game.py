import pygame as pg
from . import main_menu, sub_menus
from random import choice, random
import sys
import os
from . import settings


#Move to settings

class Game:
    """Mario game object"""
    def __init__(self):
        # Set up screen
        self.screen = pg.display.set_mode((1000, 800))#WIDTH, HEIGHT

        # Set up caption
        pg.display.set_caption('MARIO')

        # Set up clock
        self.clock = pg.time.Clock()

        self.load_data()

        self.paused = False

    def load_data(self):
        # Set up folder

        # Load images

        # Load sounds
        pass

    def run(self):
        self.playing = True
        menu = main_menu.MainMenu()
        selection = menu.show_screen()
        print(selection)
        sub_screen = sub_menus.SubMenus()
        sub_screen.draw_level_screen(0, 0, 1, 1, 400, 3)
        # Loop the music
        # pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(40)/1000#40 FPS
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        pass

    def draw(self):
        pass

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def new(self):
        pass

    def load_level(self):
        pass



def start():
    # Init pygame
    pg.init()
    # Init mixer
    pg.mixer.init()
    game = Game()
    game.run()
        
if __name__ == '__main__':
    # Init pygame
    pg.init()

    # Init mixer
    pg.mixer.init()

    game = Game()
    game.run()


