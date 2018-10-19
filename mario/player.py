import pygame as pg

class Sprite(pg.sprite.Sprite):
    """A Sprite Class"""
    def __init__(self):
        self._layer = 1
        self.groups = ()
        pg.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        pass


