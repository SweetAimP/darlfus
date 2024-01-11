import pygame as pg
from settings import *

class Spell_menu:
    def __init__(self):
        self.spell_rects = []
    
    def create_spell_rects(self, amount):
        self.spell_rects = []
        for i in range(amount):
            new_rect = pg.Rect(i * 60 + 10, SCREEN_SIZE['height'] * 0.75, 50,50)
            self.spell_rects.append(new_rect)
    
    def draw_spell_menu(self, surface, font):
        for index, rect in enumerate(self.spell_rects):
            text_surface = font.render(str(index), True, 'black')
            text_rect = text_surface.get_rect()
            text_rect.center = rect.center
            pg.draw.rect(
                surface, 'grey', rect
            )
            surface.blit(
                text_surface, text_rect
            )        
        