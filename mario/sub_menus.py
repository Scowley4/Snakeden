import pygame as pg
from os import path
from . import settings as sett


class SubMenus:

    def __init__(self):
        self.dir = path.dirname(__file__)
        self.screen = pg.display.get_surface()
        self.font_dir = path.join(self.dir, 'fonts')
        self.music_dir = path.join(self.dir, 'music')
        self.img_dir = path.join(self.dir, 'img')
        self.load_data()
        self.font_type = pg.font.Font(path.join(self.font_dir, 'Fixedsys500c.ttf'), 38)

    def load_data(self):
        self.mario = self.get_image(pg.image.load(path.join(self.img_dir, 'mario_bros.png')),
                                    177, 32, 15, 16, 0.3)
        self.mario.set_colorkey(sett.BLACK)
        self.mario_rect = self.mario.get_rect()
        #set location
        self.coin = self.get_image(pg.image.load(path.join(self.img_dir, 'item_objects.png')),
                                   0, 160, 8, 8, 0.3)
        self.coin.set_colorkey(sett.BLACK)
        self.coin_rect = self.coin.get_rect()

    def get_image(self,spritesheet, x, y, width, height, scale=1):
        image = pg.Surface((width, height))
        image.blit(spritesheet, (0,0), (x, y, width, height))
        new_w = width // scale
        new_h = height // scale
        image = pg.transform.scale(image, (int(new_w), int(new_h)))
        return image

    def draw_text(self, text, color, x, y):
        text_surface = self.font_type.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_stats(self, score, coins, world, level, time):
        self.draw_text('MARIO', sett.WHITE, sett.WIDTH * 0.1, sett.HEIGHT * 0.01)
        score = str(score)
        for i in range(6 - len(score)):
            score = '0' + score
        self.draw_text(score, sett.WHITE, sett.WIDTH * 0.1, sett.HEIGHT * 0.05)
        self.coin_rect.topleft = (sett.WIDTH * 0.35, sett.HEIGHT * 0.06)
        self.screen.blit(self.coin, self.coin_rect)
        self.draw_text(('x'+str(coins)), sett.WHITE, sett.WIDTH * 0.38, sett.HEIGHT * 0.05)
        self.draw_text('WORLD', sett.WHITE, sett.WIDTH * 0.60, sett.HEIGHT * 0.01)
        self.draw_text(str(world) + '-' + str(level), sett.WHITE, sett.WIDTH * 0.62, sett.HEIGHT * 0.05)
        self.draw_text('TIME', sett.WHITE, sett.WIDTH * 0.80, sett.HEIGHT * 0.01)
        if time is not None:
            self.draw_text(str(time), sett.WHITE, sett.WIDTH * 0.81, sett.HEIGHT * 0.05)
        #pg.display.flip()

    def draw_level_screen(self,score, coins, world, level, time, lives):
        self.screen.fill(sett.BLACK)
        self.draw_stats(score, coins, world, level, time)
        self.draw_text('WORLD '+ str(world) + '-' + str(level), sett.WHITE, sett.WIDTH * 0.40, sett.HEIGHT * 0.40)
        self.mario_rect.topleft = (sett.WIDTH * 0.42, sett.HEIGHT * 0.50)
        self.screen.blit(self.mario, self.mario_rect)
        self.draw_text('x  ' + str(lives), sett.WHITE, sett.WIDTH * 0.51, sett.HEIGHT * 0.51)
        pg.display.flip()
        pg.time.wait(800)

    def time_up_screen(self, score, coins, world, level):
        self.screen.fill(sett.BLACK)
        self.draw_stats(score, coins, world, level, None)
        self.draw_text('TIME UP', sett.WHITE, sett.WIDTH * 0.40, sett.HEIGHT * 0.50)
        pg.display.flip()

    def game_over_screen(self, score, coins, world, level):
        self.screen.fill(sett.BLACK)
        self.draw_stats(score, coins, world, level, None)
        self.draw_text('GAME OVER', sett.WHITE, sett.WIDTH * 0.40, sett.HEIGHT * 0.50)
        pg.display.flip()
        # add busy loop to wait for input

