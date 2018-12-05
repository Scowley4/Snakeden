import pygame as pg
from os import path
from . import settings
vec = pg.math.Vector2

class MapSprite(pg.sprite.Sprite):
    img_dir = path.join(path.dirname(__file__), 'img')
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)
        self.dir = path.dirname(__file__)
        self.game = game
        self.img_dir = path.join(self.dir, 'img')

        # Init rect before first image
        self.rect = pg.rect.Rect(pos, (16,16))
        self.pos = vec(*pos)

        self.last_anim_update = 0
        self.frame_count = 0
        self.iframe = 0

    def update(self):
        self._update_frame()
        self.frame_count += 1

    def _update_frame(self):
        try:
            self.frames
        except AttributeError:
            self._get_frames()
        now = pg.time.get_ticks()

        self.iframe = self.get_iframe(self.frame_count)
        self.image = self.frames[self.iframe]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        return


        # Verified to be 3 frames per image for Koopas and Goombas
        #print(now-self.last_anim_update)
        if now - self.last_anim_update > (3*settings.FPS):
            self.last_anim_update = now

            #self.iframe = (self.iframe + 1) % 2
            #self.iframe = 0
            self.iframe = self.get_iframe(self.frame_count)
            self.image = self.frames[self.iframe]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos

    @classmethod
    def get_image(cls, x, y, width, height):

        try:
            MapSprite.sprite_sheet
        except AttributeError:
            #MapSprite.sprite_sheet = pg.image.load(path.join(cls.img_dir,
            #'item_objects.png'))
            MapSprite.sprite_sheet = pg.image.load(path.join(cls.img_dir,
            'tile_set.png'))

        c = (88, 88, 88)
        image = pg.Surface([width, height]).convert()
        image.fill(c)
        rect = image.get_rect()

        image.blit(MapSprite.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c)
        image = pg.transform.scale(image, (int(rect.width * settings.SCALE),
                                           int(rect.height * settings.SCALE)))
        return image

    @classmethod
    def _get_frames(cls):
        cords = cls.frame_cords
        cls.frames = [cls.get_image(*cord) for cord in cords]

    def get_iframe(self, frame):
        try:
            return self.frame_to_img[frame % self.tot_frame_cycle]
        except AttributeError as e:
            return 0



# class Platform(MapSprite):
#     def __init__(self, game):
#         super().__init__(game)

def frame_gen(frame_lens):
    for i, frame_len in enumerate(frame_lens):
        for _ in range(frame_len):
            yield i

class Brick(MapSprite):
                   #   x,   y,   w,   h
    frame_cords = [(  16,   0,  16,  16),
                  ]
    def __init__(self, game, pos):
        super().__init__(game, pos)

class QBlock(MapSprite):
    # Cords for the item sprite sheet
                   #  x,   y,   w,   h
    frame_cords = [(   0,  80,  16,  16), #  9 frame
                   (  16,  80,  16,  16), #  3 frame
                   (  32,  80,  16,  16), #  3 frame
                   (  48,  80,  16,  16), #  3 frame
                  ]
    # Cords for the tiles sheet (which actually looks a little different)
    # The first frame here is a little too orange?
    frame_cords = [( 384,   0,  16,  16), #  9 frame
                   ( 400,   0,  16,  16), #  3 frame
                   ( 416,   0,  16,  16), #  3 frame
                   ( 400,   0,  16,  16), #  3 frame
                  ]

    frame_lens = [9, 3, 3, 3]
    tot_frame_cycle = sum(frame_lens)

    frame_to_img = {i:frame for i, frame in enumerate(frame_gen(frame_lens))}

    def __init__(self, game, pos):
        super().__init__(game, pos)


# class Coin(ItemSprite):
#     def __init__(self, game):
#         super().__init__(game)
# 
# class Tube(ItemSprite):
#     pass
