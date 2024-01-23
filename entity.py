import pygame as pg
from entities_settings import *
from utils import *
from settings import *
from healthbar import HealthBar
from spell import Spell
from abc import ABC, abstractmethod
from animation import Animation

class Entity(pg.sprite.Sprite, ABC):
    def __init__(self, game, tag, type, grid_pos, *groups):
        super().__init__(*groups)
        self.game = game
        self.map = self.game.map
        self.tag = tag
        self.type = type
        self.action = 'idle'
        self.facing = 'sw'
        self.actions = {
            "idle" : True,
            "walk" : False,
            "pre_cast": False,
            "spell_cast" : False
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
        # MOVEMENT IMAGE
        self.walking_hover = pg.image.load("assets/hovers/walking_hover.png").convert_alpha()
        self.duration = 6
        self.animations = {
            'idle':{
                "sw" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["idle"]["sw"],4,32),duration=self.duration,loop=True),
                "se" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["idle"]["se"],4,32),duration=self.duration,loop=True),
                "nw" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["idle"]["nw"],4,32),duration=self.duration,loop=True),
                "ne" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["idle"]["ne"],4,32),duration=self.duration,loop=True),
            } ,
            'walk':{
                "sw" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["walk"]["sw"],8,32),duration=2,loop=True),
                "se" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["walk"]["se"],8,32),duration=2,loop=True),
                "nw" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["walk"]["nw"],8,32),duration=2,loop=True),
                "ne" : Animation(extrac_imgs_from_sheet(self.entity_data["assets"]["walk"]["ne"],8,32),duration=2,loop=True),
            } 
        }
        self.animation = self.animations[self.action][self.facing]
        self.image = self.animation.img()
        self.rect = self.image.get_rect(topleft = self.draw_pos)

        # SPELLS
        self.spells = [Spell(self.get_instance(), settings) for settings in self.entity_data["spells"]]

        # GAMEPLAY VARIABLES
        self.usable_mp= self.mp
        self.usable_ap = self.ap
        self.playing = False
        self.steps = []
        self.directions = []
        self.current_step = 0
        self.inner_steps = []
        self.inner_step = 0

    def set_action(self, action, facing):
        if self.action != action or self.facing != facing:
            self.action = action
            self.facing = facing
            for action_key in self.actions.keys():
                if action == action_key:
                    self.actions[action_key] = True
                    if self.action in self.animations:
                        self.animation = self.animations[self.action][self.facing].copy()
                else:
                    self.actions[action_key] = False
            return True
        else:
            return False

    def update_tile(self):
        if self.tile != self.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]:
            self.tile = self.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]

    def get_instance(self):
        return self
     
    def start_turn(self):
        if self.current_health > 0:
            self.playing = True
            self.set_action('idle', self.facing)
            self.mp_used = 0
            self.usable_mp = self.mp
            self.ap_used = 0
            self.usable_ap = self.ap
            return True
        else:
            return False

    def take_damage(self, dmg):
        if self.current_health - dmg > 0:
            self.current_health -= dmg
            return False
        else:
            self.current_health = 0
            self.kill()
            return True

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
        self.inner_step = 0
        self.inner_steps = []

    def _define_movement(self, start, end, inner_steps):
        if not self.inner_steps:
            self.inner_steps.append(start)
            self.inner_steps.extend(find_interm_points(start,end, inner_steps))
            self.inner_steps.append(end)

        self.grid_pos = self.inner_steps[self.inner_step]
        facing = self.directions[self.current_step+1]
        self.set_action('walk', facing)
        if self.inner_step + 1 < len(self.inner_steps):
            self.inner_step += 1
        else:
            self.current_step += 1
            self.inner_step = 0
            self.inner_steps = []

    def move(self):
        steps = len(self.steps)
        if steps > 0 and self.usable_mp > 0:
            if steps == 1 and self.current_step < steps:
                start = self.grid_pos
                end = self.steps[self.current_step].grid_pos
                self._define_movement(start,end, 10)
            elif self.current_step + 1 < steps:
                start = self.steps[self.current_step].grid_pos
                end = self.steps[self.current_step + 1].grid_pos
                self._define_movement(start,end, 10)
            else:
                mp_used = steps
                self._update_mp(mp_used)
                self.set_action('idle', self.facing)
                self.movement_clean_up()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def end_turn(self):
        pass
    