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
            "spell_cast" : False,
            "attack" : False,
            "death": False
        }       

        # ENTITY RELATED DATA
        self.entity_data = entities[self.type]
        self.size = self.entity_data['size']
        self.mp = self.entity_data['mp']
        self.ap = self.entity_data['ap']
        self.max_health = self.entity_data['max_health']
        self.defense = self.entity_data['defense']
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
        self.animations = {
            'idle':{
                "sw" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["idle"]["sw"],4,32)),
                "se" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["idle"]["se"],4,32)),
                "nw" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["idle"]["nw"],4,32)),
                "ne" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["idle"]["ne"],4,32)),
            } ,
            'walk':{
                "sw" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["walk"]["sw"],8,32),duration=2),
                "se" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["walk"]["se"],8,32),duration=2),
                "nw" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["walk"]["nw"],8,32),duration=2),
                "ne" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["walk"]["ne"],8,32),duration=2),
            },
            'death':{
                "sw" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["death"]["sw"],12,32),duration=12,loop=False),
                "se" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["death"]["se"],12,32),duration=12,loop=False),
                "nw" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["death"]["nw"],12,32),duration=12,loop=False),
                "ne" : Animation(extrac_imgs_from_sheet(self.entity_data["animations"]["death"]["ne"],12,32),duration=12,loop=False),
            }  
        }
        self.animation = self.animations[self.action][self.facing]
        self.image = self.animation.img()
        self.rect = self.image.get_rect(topleft = self.draw_pos)

        # SPELLS
        self.spells = [Spell(self.get_instance(), self.entity_data["spells"][spell]) for spell in self.entity_data["spells"].keys()]
        # FLAGS
        self.spell_selected = None
        self.casted_spells = {} # SPELL CAST COUNTING

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
                else:
                    self.actions[action_key] = False
            if self.actions["attack"]:
                    self.animation = self.spell_selected.animations[self.facing].copy()
            elif self.action in self.animations:
                self.animation = self.animations[self.action][self.facing].copy()
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

    def death(self):
        if self.animation.done:
            self.kill()

    def calculate_incoming_damage(self, damage_taken):
        if self.defense == 0:
            return damage_taken
        else:
            return int(damage_taken * ((100-self.defense) / 100 ))

    def take_damage(self, dmg):
        final_damage = self.calculate_incoming_damage(dmg)
        if self.current_health - final_damage > 0:
            self.current_health -= final_damage
            return False
        else:
            self.current_health = 0
            return self.set_action("death", self.facing) # True

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
    