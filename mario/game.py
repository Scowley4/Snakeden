import pygame as pg
from . import main_menu, sub_menus
from random import choice, random
import sys
from os import path
from . import settings
from . import mario
from . import tilemap
from .enemies import *


font_name = pg.font.match_font('arial')

def draw_text(surface, text, size, color, x, y):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surf, text_rect)
#Move to settings

class Game:
    """Mario game object"""
    def __init__(self):
        # Set up screen
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT)) #WIDTH, HEIGHT
        print(f'Init screen as {settings.WIDTH}x{settings.HEIGHT}')

        # Set up caption
        pg.display.set_caption('MARIO')

        # Set up clock
        self.clock = pg.time.Clock()

        self.load_data()

        self.paused = False

    def load_data(self):
        # Set up folder
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'tiledlevels')
        # Load images
        self.map = tilemap.TiledMap(path.join(map_folder, 'LevelOneMap.tmx'))

        # Get map and rect
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # Scale map and get rect again
        self.map_img = pg.transform.scale(self.map_img,
                      (self.map_rect.width*int(settings.SCALE),
                    self.map_rect.height*int(settings.SCALE)))
        self.map_rect = self.map_img.get_rect()
        print(self.map_rect)
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
            self.dt = self.clock.tick(settings.FPS)/1000 #40 FPS
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.mario)
        hits = pg.sprite.spritecollide(self.mario, self.platforms, False)
        if hits:
            if self.mario.rect.top > hits[0].rect.top:
                self.mario.pos.y = hits[0].rect.bottom - (self.mario.rect.top - self.mario.pos.y)
                self.mario.vel.y = 0
            elif self.mario.pos.y < hits[0].rect.bottom:
                self.mario.pos.y = hits[0].rect.top
                self.mario.vel.y = 0


    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.screen.fill(settings.LIGHTGREY)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #self.all_sprites.draw(self.screen)
        self.sub_screen.draw_stats(0, 0, 1, 1, 400)
        self.draw_fine_grid()

        #def draw_text(surface, text, size, color, x, y):
        mouse_pos = pg.mouse.get_pos()
        draw_text(self.screen, str(mouse_pos),
                  16, settings.WHITE, 500, 10)
        draw_text(self.screen, self.get_tile_pos(*mouse_pos),
                  16, settings.WHITE, 500, 30)
        pg.display.flip()

    def get_tile_pos(self, x, y):
        pix = settings.TILESIZE
        tile_x = x//pix
        tile_y = y//pix
        return tile_x, tile_y

    def draw_fine_grid(self, show_major=True, show_minor=True):
        skip = settings.TILESIZE//2
        major = skip*2
        minor = skip
        width = 1
        major_c = settings.BLACK
        minor_c = settings.MEDGREY
        for x in range(0, settings.WIDTH, skip):
            if show_major and (x % major)==0:
                pg.draw.line(self.screen, major_c, (x, 0), (x, settings.HEIGHT), width)
            else:
                if show_minor:
                    pg.draw.line(self.screen, minor_c, (x, 0), (x, settings.HEIGHT), width)
        for y in range(0, settings.HEIGHT, skip):
            if show_major and (y % major)==0:
                pg.draw.line(self.screen, major_c, (0, y), (settings.WIDTH, y), width)
            else:
                if show_minor:
                    pg.draw.line(self.screen, minor_c, (0, y), (settings.WIDTH, y), width)
        y = 896
        pg.draw.line(self.screen, settings.RED, (0, y), (settings.WIDTH, y), 1)

    def draw_grid(self, color):
        lines = []
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, color, (x, 0), (x, settings.HEIGHT))
            for y in range(0, settings.HEIGHT, settings.TILESIZE):
                pg.draw.line(self.screen, color, (0, y), (settings.WIDTH, y))
                lines.append((x,y))
        #print(lines)

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
        self.enemies = pg.sprite.Group()

        self.mario = mario.Mario(self)
        self.all_sprites.add(self.mario)

        enemies = [Goomba(self), DudeGoomba(self),
                   KoopaTroopa(self), BuzzyBeetle(self),
                   Bowser(self)]
        # enemies = [Goomba(self)]
        for enemy in enemies:
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        for plat in settings.PLATFORM_TILES:
            p = mario.Platform(*plat, hidden=True)
            self.all_sprites.add(p)
            self.platforms.add(p)

        TILESIZE = settings.TILESIZE
        for brick in self.map.tmxdata.get_layer_by_name('block_object_layer'):
            p = mario.Platform(brick.x*settings.SCALE,
                               brick.y*settings.SCALE,
                               TILESIZE, TILESIZE,
                               settings.BLUE)
            self.platforms.add(p)
            self.all_sprites.add(p)
        for obj in self.map.tmxdata.objects:
            print(obj)
            print(obj.name)

        self.camera = tilemap.Camera(self.map.width*settings.SCALE,
                                     self.map.height*settings.SCALE)

    def load_level(self):
        pass


def start():
    # Init pygame
    pg.init()
    # Init mixer
    pg.mixer.init()
    pg.mixer.pause()
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
