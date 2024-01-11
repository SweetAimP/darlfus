from utils import *
class Spell:
    def __init__(self, spell_settings):
        self.type = spell_settings["type"]
        self.area = spell_settings["area"]
        self.range = spell_settings["range"]
        self.spell_dmg = spell_settings["damage"]
        self.ap_cost = spell_settings["ap_cost"]
    
    def draw_range(self, center):
        set_tiles = set()
        set_tiles.add(center)
        self.get_area_by_depth(center, 0, set_tiles, self.range)
        for tile in set_tiles:
            pg.display.get_surface().blit(
                pg.image.load('assets/mouse/hover.png').convert_alpha(),
                tile.draw_pos
            )
        return set_tiles
        
    def get_area_by_depth(self, center, depth, set_tiles, end_flag):
        if depth == end_flag:
            return True
        for neighbor in center.get_neighbors():
            set_tiles.add(neighbor)
            self.get_area_by_depth(neighbor, depth + 1, set_tiles, end_flag)
    
    def draw_spell_area(self, center):
        set_are_tiles = set()
        set_are_tiles.add(center)
        self.get_area_by_depth(center, 0, set_are_tiles, self.area)
        for tile in set_are_tiles:
            pg.display.get_surface().blit(
                pg.image.load('assets/mouse/spell_hover.png').convert_alpha(),
                tile.draw_pos
            )
        return set_are_tiles

    
            
            

