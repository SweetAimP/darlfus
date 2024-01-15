from utils import *
class Spell:
    def __init__(self, owner, spell_settings):
        self.owner = owner
        self.owner_tile = self.owner.map.grid[int(self.owner.grid_pos[1])][int(self.owner.grid_pos[0])]
        self.type = spell_settings["type"]
        self.area = spell_settings["area"]
        self.range = spell_settings["range"]
        self.spell_dmg = spell_settings["damage"]
        self.ap_cost = spell_settings["ap_cost"]
        self.range_tiles = []
        self.area_tiles = []

    def update_onwer_tile(self):
        if self.owner_tile != self.owner.map.grid[int(self.owner.grid_pos[1])][int(self.owner.grid_pos[0])]:
            self.owner_tile = self.owner.map.grid[int(self.owner.grid_pos[1])][int(self.owner.grid_pos[0])]
            return True
        return False

    def draw_spell_range(self, surface):
        if self.update_onwer_tile():
            set_range_tiles = set()
            set_range_tiles.add(self.owner_tile)
            self.get_area_by_depth(self.owner_tile, 0, set_range_tiles, self.range)
            self.range_tiles = set_range_tiles

        for tile in self.range_tiles:
                surface.blit(
                    pg.image.load('assets/mouse/hover.png').convert_alpha(),
                    tile.draw_pos
                )
        return self.range_tiles
        
    def draw_spell_area(self, surface, center):
        set_are_tiles = set()
        set_are_tiles.add(center)
        self.get_area_by_depth(center, 0, set_are_tiles, self.area)
        for tile in set_are_tiles:
            pg.display.get_surface().blit(
                pg.image.load('assets/mouse/spell_hover.png').convert_alpha(),
                tile.draw_pos
            )
        return set_are_tiles

    def get_area_by_depth(self, center, depth, set_tiles, end_flag):
        if depth == end_flag:
            return True
        for neighbor in center.get_neighbors():
            set_tiles.add(neighbor)
            self.get_area_by_depth(neighbor, depth + 1, set_tiles, end_flag)
    
            
            

