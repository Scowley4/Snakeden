import pygame as pg
from os import path
from . import settings
vec = pg.math.Vector2


class Mario(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.dir = path.dirname(__file__)
        self.game = game

        self.img_dir = path.join(self.dir, 'img')
        self.sprite_sheet = pg.image.load(path.join(self.img_dir, 'mario_bros.png'))

        # single image from sprite, to start
        self.image = self.get_image(178, 32, 12, 16)
        self.rect = self.image.get_rect()

        self.pos = vec(settings.WIDTH * 1/6, settings.HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # only allowed to jump if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        # if there is something below us
        if hits:
            self.vel.y = -12

    def update(self):
        # 0.5 creates gravity each frame
        self.acc = vec(0, settings.GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -settings.MARIO_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = settings.MARIO_ACC

        # defines the motion of Mario
        # no friction in the y direction
        self.acc.x += self.vel.x * settings.MARIO_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > settings.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = settings.WIDTH

        self.rect.midbottom = self.pos

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(settings.BLACK)
        image = pg.transform.scale(image, (int(rect.width * settings.SIZE_MULTIPLIER),
                                           int(rect.height * settings.SIZE_MULTIPLIER)))
        return image


class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
