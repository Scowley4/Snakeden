import pygame as pg
from random import choice, random
import sys
import os


#Move to settings
WIDTH = 500
HEIGHT = 500

def Game:
    """Mario game object"""
    def __init__(self):
        # Set up screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        # Set up caption
        pg.display.set_caption('MARIO')

        # Set up clock
        self.clock = pg.time.Clock()

        self.load_data()

    def load_data(self):
        # Set up folder

        # Load images

        # Load sounds
        pass

    def run(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def events(self):
        pass

    def new(self):
        pass

    def load_level(self):
        pass


if __name__ == '__main__':
    # Init pygame
    pygame.init()

    # Init mixer
    pygame.mixer.init()


