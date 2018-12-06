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
        self.load_images()
        self.image = self.standing_frame_r
        self.rect = self.image.get_rect()
        self.last_update = 0
        self.current_frame = 0

        self.pos = vec(settings.WIDTH * 1/6, settings.HEIGHT * .8)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False

    def load_images(self):
        self.standing_frame_l = self.get_image(178, 32, 12, 16)
        self.standing_frame_l.set_colorkey(settings.BLACK)

        self.standing_frame_r = pg.transform.flip(self.standing_frame_l, True, False)

        self.walk_frames_l = [self.get_image(80, 32, 15, 17), self.get_image(95, 32, 15, 17),
                              self.get_image(114, 32, 15, 16)]
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            frame.set_colorkey(settings.BLACK)
            self.walk_frames_r.append(pg.transform.flip(frame, True, False))
        self.jump_frame_l = self.get_image(144, 32, 16, 16)
        self.jump_frame_l.set_colorkey(settings.BLACK)

        self.jump_frame_r = pg.transform.flip(self.jump_frame_l, True, False)

    def reset(self):
        self.pos = vec(settings.WIDTH * 1/6, settings.HEIGHT * .8)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # only allowed to jump if standing on a platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        # if there is something below us
        if hits:
            self.jumping = True
            self.vel.y = -8*settings.SCALE

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        self.animate()
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
        if abs(self.vel.x) < .1:
            self.vel.x = 0

        if self.vel.y > settings.MAX_DOWN:
            self.vel.y = settings.DOWN_RESET
        self.pos += self.vel + 0.5 * self.acc

        # print(self.vel)
        # print(self.acc)

        self.rect.midbottom = self.pos

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(settings.BLACK)
        image = pg.transform.scale(image, (int(rect.width * settings.SCALE),
                                           int(rect.height * settings.SCALE)))
        print(image.get_rect().width)
        return image


class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h, color=settings.GREEN, hidden=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        if hidden:

            self.image.set_colorkey(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



