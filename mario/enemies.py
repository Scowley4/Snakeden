import pygame as pg
from os import path
from . import settings
vec = pg.math.Vector2


# class GeneralEnemy(Enemy):
#     """"""
#     def __init__(self, game):
#         pg.sprite.Sprite.__init__(self)


class Enemy(pg.sprite.Sprite):
    """General class for enemies.

    Probably reserve this for moving ground enimies? Make something else for
    PiranhaPlants, BulletBill (and BillBlaster), CheepCheep, Lakitu, etc.
    """

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.dir = path.dirname(__file__)
        self.game = game

        self.img_dir = path.join(self.dir, 'img')
        # self.sprite_sheet = pg.image.load(path.join(self.img_dir, 'mario_bros.png'))

        # single image from sprite, to start
        # self.image = self.get_image(178, 32, 12, 16)
        # self.rect = self.image.get_rect()

        # self.pos = vec(settings.WIDTH * 1/6, settings.HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        # 0.5 creates gravity each frame
        self.acc = vec(0, settings.GRAVITY)

        # TODO - research
        # I think enemies in mario only have a fixed velocity.

        # self.acc.x += self.vel.x * settings.MARIO_FRICTION
        # self.vel += self.acc
        # self.pos += self.vel + 0.5 * self.acc


        self.rect.midbottom = self.pos

    def get_image(self, x, y, width, height):
        # TODO - What is the purpose of this function?
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(settings.BLACK)
        image = pg.transform.scale(image, (int(rect.width * settings.SIZE_MULTIPLIER),
                                           int(rect.height * settings.SIZE_MULTIPLIER)))
        return image

class Goomba(Enemy):
    """"""
    def __init__(self, game):
        super().__init__(game)

class KoopaTroopa(Enemy):
    """"""
    def __init__(self, game):
        super().__init__(game)


class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
