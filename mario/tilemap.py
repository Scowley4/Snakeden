import pygame as pg
import pytmx
from . import settings

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    # apply the offset to a sprite
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    # apply the offset to a rectangle
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(settings.WIDTH * .5)
        y = -target.rect.bottom + int(settings.HEIGHT * .85)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - settings.WIDTH), x)
        y = max(-(self.height - settings.HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)







