from entity import Entity
from utils import *

class Player(Entity):
    def __init__(self, map, tag, type, image, grid_pos, *groups):
        super().__init__(map, tag, type, image, grid_pos, *groups)
        self.map = map
        # FLAGS
        self.spell_casting = False
        self.spell_selected = None
        self.start_action_flag = False
    
    def end_turn(self):
        self.playing = False
        self.spell_casting = False
        self.moving = False
        self.start_action_flag = False
        self.movement_clean_up()
        
    def move(self):
        if len(self.steps) > 0 and self.usable_mp > 0:
            self.grid_pos = self.steps[self.current_step].grid_pos
            if self.current_step + 1 < len(self.steps):
                self.current_step += 1
            else:
                mp_used = len(self.steps)
                self._update_mp(mp_used)
                self.end_action()
                self.movement_clean_up()

    def _cast_dmg_spell(self):
        self.map.get_attacked_entities(self.spell_selected.area_tiles, self.spell_selected.spell_dmg)
    
    def _cast_mov_spell(self):
        target_tile = list(self.spell_selected.area_tiles)[0]
        if target_tile.status == 0:
            self.grid_pos = target_tile.grid_pos
            return True
        return False
    
    def cast_spell(self):
        if self.usable_ap >= self.spell_selected.ap_cost:
            if self.spell_selected.type == "dmg":
                self._cast_dmg_spell()
            elif self.spell_selected.type == "mov":
                self._cast_mov_spell()

            self._update_ap(self.spell_selected.ap_cost)
        self.end_action()
        
        
    def end_action(self):
        self.start_action_flag = not self.start_action_flag
        if self.spell_casting:
            self.spell_casting = not self.spell_casting
        
    def start_action(self):
        self.start_action_flag = not self.start_action_flag

    def draw_movement(self, surface):
            recons_path, _ = self.map.get_walking_path()
            if not self.steps:
                if recons_path:
                    for node in recons_path:
                        surface.blit(
                            node.hover_img,
                            node.rect.topleft
                        )
                    if self.start_action_flag:
                        self.steps = recons_path
                        self.directions = _
                else:
                    return False
    
    def draw_spell_casting(self,surface):
        range_tiles = self.spell_selected.draw_spell_range(surface)
        hover_tile = self.map.get_hover_tile()
        if hover_tile and hover_tile in range_tiles:
            self.spell_selected.draw_spell_area(surface, hover_tile)
                
    def draw(self, surface):
        if self.moving:
            self.draw_movement(surface)
        elif self.spell_casting:
            self.draw_spell_casting(surface)

        surface.blit(
            self.image,
            self.draw_pos
        )
        self.health_bar.draw(surface)
    
    def update(self):
        self.update_tile()
        if self.start_action_flag:
            if self.moving:
                self.move()
            elif self.spell_casting:
                self.cast_spell()
        self._update_draw_pos()
        self._update_rect()