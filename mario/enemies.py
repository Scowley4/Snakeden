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
    img_dir = path.join(path.dirname(__file__), 'img')

    def __init__(self, game):
        print('Enemy __init__')
        pg.sprite.Sprite.__init__(self)
        self.dir = path.dirname(__file__)
        self.game = game

        # self.sprite_sheet = pg.image.load(path.join(self.img_dir, 'mario_bros.png'))

        # single image from sprite, to start
        # self.image = self.get_image(178, 32, 12, 16)
        # self.rect = self.image.get_rect()
        self.last_anim_update = 0
        self.iframe = 0

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def collide_with_platforms(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #print('pos', self.pos.y)

        if hits:
            if self.vel.y > 0 and self.pos.y > hits[0].rect.top:
                self.pos.y = hits[0].rect.top
        #        print()
        #        print(hits[0].rect.top)
        #        print(self.rect.height)
        #        print()
            if self.vel.y < 0:
                self.pos.y = hits[0].rect.bottom
            self.vel.y = 0
            self.rect.y = self.pos.y

    def update(self):
        # 0.5 creates gravity each frame
        self.acc = vec(0, settings.GRAVITY)

        # TODO - research
        # I think enemies in mario only have a fixed velocity.

        self.acc.x += self.vel.x * settings.MARIO_FRICTION
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < .1:
            self.vel.y = 0 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self._update_frame()
        self.collide_with_platforms()


        self.rect.midbottom = self.pos

    def stopy(self):
        self.vel.y = 0

    def _update_frame(self):
        try:
            self.frames
        except AttributeError:
            self._get_frames()
        now = pg.time.get_ticks()

        # Verified to be 3 frames per image for Koopas and Goombas
        #print(now-self.last_anim_update)
        if now - self.last_anim_update > (3*settings.FPS):
            self.last_anim_update = now

            #self.iframe = (self.iframe + 1) % 2
            #self.iframe = 0
            self.iframe = (self.iframe + 1) % 2
            self.image = self.frames[self.iframe]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos


    @classmethod
    def get_image(cls, x, y, width, height):

        try:
            Enemy.sprite_sheet
        except AttributeError:
            Enemy.sprite_sheet = pg.image.load(path.join(cls.img_dir, 'enemies.png'))

        # XXX This is the only way I could get the filling to work. Normally,
        #     when you make a new image, it fills with black. Then when I tried
        #     to set_colorkey, it would also fill in the goomba black features
        #     with transparent. So I ended up filling the image with a random
        #     color first, then setting the color key to that color. Seems like
        #     it might be a workaround. Anyone know a better way?
        c = (88, 88, 88)
        image = pg.Surface([width, height]).convert()
        image.fill(c)
        rect = image.get_rect()

        image.blit(Enemy.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c)
        image = pg.transform.scale(image, (int(rect.width * settings.SCALE),
                                           int(rect.height * settings.SCALE)))
        return image

    @classmethod
    def _get_frames(cls):
        cords = cls.frame_cords
        cls.frames = [cls.get_image(*cord) for cord in cords]

def tnp(val):
    return (val//4)*4

class Goomba(Enemy):
    """"""
                   # x,  y,  w,  h
    frame_cords = [( 0, 16, 16, 16), # walk 1
                   (16, 16, 16, 16), # walk 2
                   (32, 16, 16, 16), # squish
                  ]
    def __init__(self, game):
        print('Goomba __init__')
        super().__init__(game)
        x = settings.WIDTH * 1/32
        print('x pos', x)
        x = tnp(x)
        print('new x pos', x)

        y = settings.HEIGHT * .4
        y = settings.HEIGHT * .8
        print('y pos', y)
        self.pos = vec(x, y)

class DudeGoomba(Enemy):
    """"""
                   # x,  y,  w,  h
    frame_cords = [(48, 16, 16, 16), # walk 1
                   (64, 16, 16, 16), # walk 2
                   (80, 16, 16, 16), # squish
                  ]
    def __init__(self, game):
        print('Goomba __init__')
        super().__init__(game)
        self.pos = vec(settings.WIDTH * 3/32, settings.HEIGHT * .4)


class KoopaTroopa(Enemy):
    """"""
                   #  x,   y,  w,  h
    frame_cords = [( 96,  8, 16, 24), # walk 1
                   (112,  8, 16, 24), # walk 2
                   (128,  8, 16, 24), # squish
                  ]
    def __init__(self, game):
        print('KoopaTroopa __init__')
        super().__init__(game)
        self.pos = vec(settings.WIDTH * 5/32, settings.HEIGHT * .4)

class BuzzyBeetle(Enemy):
    """"""
                   #  x,   y,  w,  h
    frame_cords = [(512, 16, 16, 16), # walk 1
                   (528, 16, 16, 16), # walk 2
                   (544, 16, 16, 16), # squish
                  ]
    def __init__(self, game):
        print('BuzzyBeetle __init__')
        super().__init__(game)
        self.pos = vec(settings.WIDTH * 7/32, settings.HEIGHT * .4)

class Bowser(Enemy):
    """"""
                   #  x,   y,  w,  h
    frame_cords = [(656,   0, 32, 32), # mouth open - walk 1
                   (688,   0, 32, 32), # mouth open - walk 1
                   (720,   0, 32, 32), # mouth open - walk 1
                   (752,   0, 32, 32), # mouth open - walk 1
                  ]
    def __init__(self, game):
        print('Bowser __init__')
        super().__init__(game)
        self.pos = vec(settings.WIDTH * 9/32, settings.HEIGHT * .4)


class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
