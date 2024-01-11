import pygame as pg
from character import Character


class Enemy(Character):
    def __init__(self, pos, type, image, tag, *groups):
        super().__init__(pos, type, image, tag, *groups)
