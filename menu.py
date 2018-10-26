
import pygame as pg
from mario import settings
from os import path


class Menu:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption("Snakeden Arcade")
        self.load_data()
        self.at_menu = True

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')

    def start_screen(self):
        self.show_menu()
        while self.at_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.at_menu = False

    def show_menu(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'menu.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(settings.BLACK)

    def draw_text(self, text, size, color, font_type, x, y):
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_image(self, image, x, y):
        img = pg.image.load(image).convert()
        img_rect = img.get_rect()
        img_rect.midtop = (x,y)
        self.screen.blit(img, img_rect)


menu = Menu()
menu.start_screen()
pg.QUIT

