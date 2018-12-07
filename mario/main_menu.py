from . import settings as sett
from os import path
import pygame as pg


class MainMenu:

    def __init__(self):
        self.dir = path.dirname(__file__)
        self.screen = pg.display.get_surface()
        self.img_dir = path.join(self.dir, 'img')
        self.music_dir = path.join(self.dir, 'music')
        self.font_dir = path.join(self.dir, 'fonts')
        self.exit = False
        self.cursor_x = 270
        self.cursor_y = [450, 500, 550, 600]
        self.list_len = len(self.cursor_y)
        self.selection = 0
        self.ground_y = sett.HEIGHT - 50
        self.ground_x = 17
        self.spritesheet_menu = pg.image.load(path.join(self.img_dir, 'title_screen.png'))
        self.spritesheet_mario = pg.image.load(path.join(self.img_dir, 'mario_bros.png'))
        self.spritesheet_tiles = pg.image.load(path.join(self.img_dir, 'tile_set.png'))
        self.font_type = pg.font.Font(path.join(self.font_dir, 'Fixedsys500c.ttf'), 42)
        self.load_data()

    def get_image(self,spritesheet, x, y, width, height, scale=1):
        image = pg.Surface((width, height))
        image.blit(spritesheet, (0,0), (x, y, width, height))
        new_w = width // scale
        new_h = height // scale
        image = pg.transform.scale(image, (int(new_w), int(new_h)))
        return image

    def set_cursor(self):
        # extract from sprite sheet
        self.cursor = self.get_image(self.spritesheet_menu, 3, 155, 8, 8, 0.2)
        self.cursor.set_colorkey(self.color_key)
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.midtop = (self.cursor_x, self.cursor_y[0])

    def set_title(self):
        # extract image from spritesheet
        self.title = self.get_image(self.spritesheet_menu, 1, 60, 176, 88, 0.3)
        # make pink pixels transparent
        self.color_key = self.title.get_at((0,0))
        self.title.set_colorkey(self.color_key)
        # set rect varaible
        self.title_rect = self.title.get_rect()
        self.title_rect.midtop = (sett.MID_X, sett.HEIGHT / 9)

    def set_mario(self):
        self.mario = self.get_image(self.spritesheet_mario, 178, 32, 12, 16, 0.2)
        self.mario.set_colorkey(sett.BLACK)
        self.mario_rect = self.mario.get_rect()
        self.mario_rect.midbottom = (self.ground_x + 100, self.ground_y - 105)

    def set_ground(self):
        self.ground = self.get_image(self.spritesheet_tiles, 0, 0, 15, 15, 0.3)
        self.ground_rect = self.ground.get_rect()
        self.ground_rect.midtop = (self.ground_x, self.ground_y)

    def set_pipe(self):
        self.pipe = self.get_image(self.spritesheet_tiles, 0, 160, 32, 32, 0.3)
        self.pipe.set_colorkey(sett.BLACK)
        self.pipe_rect = self.pipe.get_rect()
        self.pipe_rect.midbottom = (self.ground_x + 100, self.ground_y)

    def draw_text(self, text, color, x, y):
        text_surface = self.font_type.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        self.set_title()
        self.set_cursor()
        self.set_ground()
        self.set_pipe()
        self.set_mario()
        pg.mixer.music.load(path.join(self.music_dir, 'main_theme.ogg'))

    def show_screen(self):
        pg.mixer.music.play(loops=-1)
        while not self.exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        self.selection = (self.selection + 1) % self.list_len
                    if event.key == pg.K_UP:
                        self.selection = (self.selection - 1) % self.list_len
                    if event.key == pg.K_RETURN:
                        pg.mixer.music.fadeout(1000)
                        return self.selection
            self.draw_menu()
        pg.mixer.music.stop()
        return 'exit'

    def draw_menu(self):
        self.screen.fill((98,131,239))
        self.screen.blit(self.title, self.title_rect)
        self.cursor_rect.midtop = (self.cursor_x, self.cursor_y[self.selection])
        self.screen.blit(self.cursor, self.cursor_rect)
        # draw ground tiles
        for i in range(22):
            self.screen.blit(self.ground, self.ground_rect)
            self.ground_x += 50
            self.ground_rect.midtop = (self.ground_x, self.ground_y)
        self.ground_x = 17
        self.ground_rect.midtop = (self.ground_x, self.ground_y)
        # draw the pipe
        self.screen.blit(self.pipe, self.pipe_rect)
        # draw mario
        self.screen.blit(self.mario, self.mario_rect)
        # draw text menu
        self.draw_text("1-Player Game", sett.BLACK, sett.MID_X, 450)
        self.draw_text("2-Player Game", sett.BLACK, sett.MID_X, 500)
        self.draw_text("Load Level", sett.BLACK, sett.MID_X, 550)
        self.draw_text("Settings", sett.BLACK, sett.MID_X, 600)
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    pg.mixer.init()
    pg.display.set_mode((sett.WIDTH, sett.HEIGHT))
    pg.display.set_caption("MENU TEST")
    start = MainMenu()
    start.show_screen()
    pg.quit()
