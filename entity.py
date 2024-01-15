import pygame as pg
from entities_settings import *
from utils import *
from settings import *
from healthbar import HealthBar
from spell import Spell
from abc import ABC, abstractmethod

class Entity(pg.sprite.Sprite, ABC):
    def __init__(self, map, tag, type, image, grid_pos, *groups):
        super().__init__(*groups)
        self.tag = tag
        self.map = map       

        # ENTITY RELATED DATA
        self.entity_data = entities[type]
        self.size = self.entity_data['size']
        self.mp = self.entity_data['mp']
        self.ap = self.entity_data['ap']
        self.max_health = self.entity_data['max_health']
        self.current_health = self.max_health
        self.initiative = self.entity_data['initiative']
        self.health_bar = HealthBar(self.get_instance())

        # DRAW AND POSITIONING
        self.grid_pos = pg.Vector2(grid_pos)
        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + OVERGRID_DRAW_OFFSET
        self.image = image
        self.rect = self.image.get_rect(topleft = self.draw_pos)

        # SPELLS
        self.spells = [Spell(self.get_instance(), settings) for settings in self.entity_data["spells"]]




        # GAMEPLAY VARIABLES
        self.mp_used = 0
        self.usable_mp= self.mp
        self.ap_used = 0
        self.usable_ap = self.ap
        self.playing = False
        self.moving = False
        self.steps = []
        self.directions = []
        self.current_step = 0

    def get_instance(self):
        return self
     
    def start_turn(self):
        self.playing = True
        self.moving = True
        self.mp_used = 0
        self.usable_mp = self.mp
        self.ap_used = 0
        self.usable_ap = self.ap

    def take_damage(self, dmg):
        if self.current_health - dmg > 0:
            self.current_health -= dmg
        else:
            self.current_health = 0

    def _update_rect(self):
        self.rect.topleft = self.draw_pos

    def _update_draw_pos(self):
        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + OVERGRID_DRAW_OFFSET

    def _update_ap(self):
        self.usable_ap = self.ap - self.ap_used

    def _update_mp(self):
        self.usable_mp = self.mp - self.mp_used
    
    def draw(self, surface):
        surface.blit(
            self.image,
            self.draw_pos
        )
        self.health_bar.draw(surface)
   
    def movement_clean_up(self):
        self.steps = []
        self.directions = []
        self.current_step = 0
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def end_turn(self):
        pass
    