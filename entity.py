import pygame as pg
from entities_settings import *
from utils import *
from settings import *
from healthbar import HealthBar
from spell import Spell
from abc import ABC, abstractmethod
from animation import Animation

class Entity(pg.sprite.Sprite, ABC):
    def __init__(self, game, tag, type, image, grid_pos, *groups):
        super().__init__(*groups)
        self.game = game
        self.map = self.game.map
        self.tag = tag
        self.type = type
        self.action = 'idle'
        self.actions = {
            "idle" : True,
            "moving" : False,
            "pre_casting": False,
            "spell_casting" : False
        }       

        # ENTITY RELATED DATA
        self.entity_data = entities[self.type]
        self.size = self.entity_data['size']
        self.mp = self.entity_data['mp']
        self.ap = self.entity_data['ap']
        self.max_health = self.entity_data['max_health']
        self.current_health = self.max_health
        self.initiative = self.entity_data['initiative']
        self.health_bar = HealthBar(self.get_instance())

        # DRAW AND POSITIONING
        self.grid_pos = pg.Vector2(grid_pos)
        self.tile = self.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]
        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + OVERGRID_DRAW_OFFSET
        # ANIMATION
        self.duration = 6
        self.extraction_structure =  dict({'sw':[],'se':[],'nw':[],'ne':[]})
        self.idle_imgs = extrac_imgs_from_sheet('assets/entities/player/idle/wolf-idle.png',(4,4),self.extraction_structure,32,16)
        self.run_imgs = extrac_imgs_from_sheet('assets/entities/player/walk/wolf-run.png',(8,4),self.extraction_structure,32,16)
        self.animations = {
            'idle': Animation(self.idle_imgs['sw'],duration=self.duration,loop=True),
            'idle/se': Animation(self.idle_imgs['se'],duration=self.duration,loop=True),
            'idle/nw': Animation(self.idle_imgs['nw'],duration=self.duration,loop=True),
            'idle/ne': Animation(self.idle_imgs['ne'],duration=self.duration,loop=True),
            'moving': Animation(self.run_imgs['sw'],duration=self.duration,loop=True),
            'run/se': Animation(self.run_imgs['se'],duration=self.duration,loop=True),
            'run/nw': Animation(self.run_imgs['nw'],duration=self.duration,loop=True),
            'run/ne': Animation(self.run_imgs['ne'],duration=self.duration,loop=True)
        }
        self.animation = self.animations[self.action]
        self.image = image
        self.rect = self.image.get_rect(topleft = self.draw_pos)

        # SPELLS
        self.spells = [Spell(self.get_instance(), settings) for settings in self.entity_data["spells"]]

        # GAMEPLAY VARIABLES
        self.usable_mp= self.mp
        self.usable_ap = self.ap
        self.playing = False
        self.moving = False
        self.steps = []
        self.directions = []
        self.current_step = 0

    def set_action(self, action):
        if self.action != action:
            self.action = action
            for action_key in self.actions.keys():
                if action == action_key:
                    self.actions[action_key] = True
                    self.animation = self.animations[self.action].copy()
                else:
                    self.actions[action_key] = False

    def update_tile(self):
        if self.tile != self.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]:
            self.tile = self.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]

    def get_instance(self):
        return self
     
    def start_turn(self):
        self.playing = True
        self.set_action('idle')
        self.mp_used = 0
        self.usable_mp = self.mp
        self.ap_used = 0
        self.usable_ap = self.ap

    def take_damage(self, dmg):
        if self.current_health - dmg > 0:
            self.current_health -= dmg
        else:
            self.current_health = 0
            # self.game.Kill_entity(self)

    def _update_rect(self):
        self.rect.topleft = self.draw_pos

    def _update_draw_pos(self):
        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + OVERGRID_DRAW_OFFSET

    def _update_ap(self, ap_used):
        self.usable_ap -= ap_used

    def _update_mp(self, mp_used):
        self.usable_mp -= mp_used
    
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
    
    def move(self):
        if len(self.steps) > 0 and self.usable_mp > 0:
            self.grid_pos = self.steps[self.current_step].grid_pos
            if self.current_step + 1 < len(self.steps):
                self.current_step += 1
            else:
                mp_used = len(self.steps)
                self._update_mp(mp_used)
                self.set_action('idle')
                self.movement_clean_up()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def end_turn(self):
        pass
    