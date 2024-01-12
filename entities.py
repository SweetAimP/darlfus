import pygame as pg

class Entities(pg.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

    def draw(self, surface):
        sprites = self.sprites()
        for spr in sprites:
            spr.draw(surface)
            
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)