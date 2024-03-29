from utils import *
from animation import Animation
class Spell:
    def __init__(self, owner, spell_settings):
        self.owner = owner
        self.owner_tile = None
        self.max_usages = spell_settings["max_usages"]
        self.remaining_uses = self.max_usages # USED WHEN CALCULATING THE BEST COMBO AT ENEMY LVL
        self.name = spell_settings["name"]
        self.type = spell_settings["type"]
        self.subtype = spell_settings["subtype"]
        self.area = spell_settings["area"]
        self.range = spell_settings["range"]
        self.spell_dmg = spell_settings["damage"]
        self.ap_cost = spell_settings["ap_cost"]
        self.range_tiles = None
        self.area_tiles = None
        self.spell_area_center = None
        # IMAGES FOR HOVERING
        self.hover_img = pg.image.load('assets/hovers/hover.png').convert_alpha()
        self.spell_area_img = pg.image.load('assets/hovers/spell_area.png').convert_alpha()
        # Animations
        self.animations = {
            "sw" : Animation(extrac_imgs_from_sheet(spell_settings["animations"]["sw"], spell_settings["animations"]["frames"], 32), loop=False),
            "se" : Animation(extrac_imgs_from_sheet(spell_settings["animations"]["se"], spell_settings["animations"]["frames"], 32), loop=False),
            "nw" : Animation(extrac_imgs_from_sheet(spell_settings["animations"]["nw"], spell_settings["animations"]["frames"], 32), loop=False),
            "ne" : Animation(extrac_imgs_from_sheet(spell_settings["animations"]["ne"], spell_settings["animations"]["frames"], 32), loop=False),
        }

    def _update_onwer_tile(self):
        if self.owner_tile != self.owner.tile:
            self.owner_tile = self.owner.tile
            return True
        return False
    
    def _update_spell_area_center(self, center):
        if self.spell_area_center != center:
            self.spell_area_center = center
            return True
        return False
    
    def _draw_tile_hovers(self, surface, tiles, type):
        for tile in tiles:
                if tile.status in (0,2):
                    img = self.hover_img if type == 'range' else (self.spell_area_img if type == 'area' else False)
                    surface.blit(
                        img,
                        tile.draw_pos
                    )
                    
    def set_area_tiles(self, center, type, range_modifier = 0):
        limit = self.area if type == 'area' else (self.range + range_modifier if type == 'range' else False)
        set_are_tiles = set()
        set_are_tiles.add(center)
        self.get_area_by_depth(center, 0, set_are_tiles, limit)
        return set_are_tiles if center.status in (0,2) else None 

    def aplly_effect(self, target):
        if self.subtype != None:
            for subtype in self.subtype.keys():
                if subtype == 'debuff':
                    for effect in self.subtype[subtype]:
                        if effect =="defense":
                            target.defense += self.subtype[subtype][effect]

                elif subtype == 'buff':
                    for effect in self.subtype[subtype]:
                        if effect =="vampirism":
                           self.owner.current_health = min(self.owner.max_health, self.owner.current_health + int(self.spell_dmg * (self.subtype[subtype][effect] / 100)))

    def draw_spell_range(self, surface):
        if self._update_onwer_tile():
            self.range_tiles = self.set_area_tiles(self.owner_tile, 'range')
        self._draw_tile_hovers(surface, self.range_tiles, 'range')
        return self.range_tiles
  
    def draw_spell_area(self, surface, center):
        if self._update_spell_area_center(center):
            self.area_tiles = self.set_area_tiles(center, 'area')
        if self.area_tiles:
            self._draw_tile_hovers(surface, self.area_tiles, 'area')
        return self.area_tiles

    def get_area_by_depth(self, center, depth, set_tiles, end_flag):
        if depth == end_flag:
            return True
        for neighbor in center.get_neighbors():
            set_tiles.add(neighbor)
            self.get_area_by_depth(neighbor, depth + 1, set_tiles, end_flag)
    