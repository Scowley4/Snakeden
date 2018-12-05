import pygame as pg
from . import main_menu, sub_menus
from random import choice, random
import sys
from os import path
from . import settings
from . import mario
from . import tilemap
from . import item_sprites
from .enemies import *

# DEBUG controls the drawing of debugging tools:
# - Grid
# - Mouse position (screen-relative and map-relative (truepos))
DEBUG = True

font_name = pg.font.match_font('arial')

def draw_text(surface, text, size, color, x, y, align='nw'):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect()
    if align == 'nw':
        text_rect.topleft = (x, y)
    if align == 'ne':
        text_rect.topright = (x, y)
    if align == 'sw':
        text_rect.bottomleft = (x, y)
    if align == 'se':
        text_rect.bottomright = (x, y)
    if align == 'n':
        text_rect.midtop = (x, y)
    if align == 's':
        text_rect.midbottom = (x, y)
    if align == 'e':
        text_rect.midright = (x, y)
    if align == 'w':
        text_rect.midleft = (x, y)
    if align == 'center':
        text_rect.center = (x, y)
    surface.blit(text_surf, text_rect)


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




        if DEBUG:
            self._draw_debug()
        pg.display.flip()

    def _draw_debug(self):
        self.draw_fine_grid()

        #def draw_text(surface, text, size, color, x, y):
        draw_text(self.screen, 'Screen', 16, settings.WHITE, 100, 100)
        draw_text(self.screen, 'TruePos', 16, settings.WHITE, 200, 100)


        draw_text(self.screen, 'Pixel', 16, settings.WHITE, 20, 120)
        mouse_pos = pg.mouse.get_pos()
        draw_text(self.screen, str(mouse_pos),
                  16, settings.WHITE, 100, 120)
        draw_text(self.screen, self.get_tile_pos(*mouse_pos),
                  16, settings.WHITE, 100, 140)

        true_pos = self.camera.screen_to_true(mouse_pos)
        draw_text(self.screen, 'Tile', 16, settings.WHITE, 20, 140)
        draw_text(self.screen, str(true_pos),
                  16, settings.WHITE, 200, 120)
        draw_text(self.screen, self.get_tile_pos(*true_pos),
                  16, settings.WHITE, 200, 140)

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
        self.qblocks = pg.sprite.Group()

        self.mario = mario.Mario(self)
        self.all_sprites.add(self.mario)

        enemies = [Goomba(self), DudeGoomba(self),
                   KoopaTroopa(self), BuzzyBeetle(self),
                   Bowser(self)]
        # enemies = [Goomba(self)]
        for enemy in enemies:
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        qblock = item_sprites.QBlock(self, (500, 500))
        self.all_sprites.add(qblock)

        brick = item_sprites.Brick(self, (100, 800))
        self.all_sprites.add(brick)

        brick = item_sprites.Brick(self, (300, 800))
        self.all_sprites.add(brick)

        for plat in settings.PLATFORM_TILES:
            p = mario.Platform(*plat, hidden=True)
            self.all_sprites.add(p)
            self.platforms.add(p)

        TILESIZE = settings.TILESIZE
        # TODO The layers are not consistantly named in the files.
        #      Try/except here for when we try to run level 2
        try:
            for brick in self.map.tmxdata.get_layer_by_name('block_object_layer'):
                p = mario.Platform(brick.x*settings.SCALE,
                                   brick.y*settings.SCALE,
                                   TILESIZE, TILESIZE,
                                   settings.BLUE)
                self.platforms.add(p)
                self.all_sprites.add(p)
        except:
            pass
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
