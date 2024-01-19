import sys
import pygame as pg
from random import randint,randrange

GRID_DRAW_OFFSET = pg.Vector2(305,60)
TILE_TYPE_2_OFFSET = pg.Vector2(0,16)
OVERGRID_DRAW_OFFSET = pg.Vector2(305,44)
SCREEN_SIZE = {
    "width":640,
    "height":480
}
FPS = 60
ENTITIES_IMGS = [
    'assets/entities/player/player.png',
    'assets/entities/enemy.png'
]
TILE_IMAGES = [
    "assets/tiles/basic_tile.png",
    "assets/tiles/basic_tile_darker.png",
    "assets/tiles/void.png"
]