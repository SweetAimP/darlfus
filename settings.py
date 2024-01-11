import sys
import pygame as pg
from random import randint,randrange

GRID_DRAW_OFFSET = pg.Vector2(305,60)
OVERGRID_DRAW_OFFSET = pg.Vector2(305,44)
SCREEN_SIZE = {
    "width":640,
    "height":480
}
FPS = 60
CHARACTERS_IMG = [
    'assets/player/player.png',
    'assets/player/enemy.png'
]