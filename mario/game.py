import pygame as pg
from . import main_menu, sub_menus
from random import choice, random
import sys
import os
from . import settings
from . import mario


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
        self.sub_screen = sub_menus.SubMenus()
        self.sub_screen.draw_level_screen(0, 0, 1, 1, 400, 3)
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
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.mario, self.platforms, False)
        if hits:
            if self.mario.rect.top > hits[0].rect.top:
                self.mario.pos.y = hits[0].rect.bottom - (self.mario.rect.top - self.mario.pos.y)
                self.mario.vel.y = 0
            elif self.mario.pos.y < hits[0].rect.bottom:
                self.mario.pos.y = hits[0].rect.top
                self.mario.vel.y = 0

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.all_sprites.draw(self.screen)
        self.sub_screen.draw_stats(0, 0, 1, 1, 400)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.mario.jump()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.mario = mario.Mario(self)
        self.all_sprites.add(self.mario)

        for plat in settings.PLATFORM_LIST:
            p = mario.Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

    def load_level(self):
        pass


def start():
    # Init pygame
    pg.init()
    # Init mixer
    pg.mixer.init()
    game = Game()
    game.new()
    game.run()
        
if __name__ == '__main__':
    # Init pygame
    pg.init()

    # Init mixer
    pg.mixer.init()

    game = Game()
    game.new()
    game.run()


