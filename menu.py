
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
        self.draw_text("Snakeden Arcade", 68, settings.WHITE, 'arial',
                       settings.WIDTH/2, settings.HEIGHT * 1/10)
        self.draw_text("Select a game", 42, settings.WHITE, 'arial',
                       settings.WIDTH/2, settings.HEIGHT * 1/5 + 20)
        self.draw_image('mariobros_titlebox.PNG', settings.WIDTH/2, settings.HEIGHT * 1/3, 1.5)
        self.draw_text("Shoots and Ladders", 64, settings.GREEN, 'arial',
                       settings.WIDTH/2, settings.HEIGHT * 3/4 - 20)
        pg.display.flip()

    def draw_text(self, text, size, color, font_name, x, y):
        font_type = pg.font.match_font(font_name)
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def draw_image(self, image, x, y, trans):
        img = pg.image.load(path.join(self.img_dir, image)).convert()
        width = img.get_size()[0]
        height = img.get_size()[1]
        img = pg.transform.scale(img, (width//int(trans), height//int(trans)))
        img_rect = img.get_rect()
        img_rect.midtop = (x,y)
        self.screen.blit(img, img_rect)


menu = Menu()
menu.start_screen()
pg.QUIT

