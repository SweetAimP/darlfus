from entity import Entity
from utils import *

class Player(Entity):
    def __init__(self, game, tag, type, grid_pos, *groups):
        super().__init__(game, tag, type, grid_pos, *groups)
        
        # MOVEMENT IMAGE
        self.walking_hover = pg.image.load("assets/hovers/walking_hover.png").convert_alpha()
        # FLAGS
        self.spell_selected = None
        self.start_action_flag = False

        # SPELL CAST COUNTING
        self.casted_spells = {}
    
    def get_animation(self):
        pass

    def end_turn(self):
        self.playing = False
        self.casted_spells = {}
        self.movement_clean_up()
    
    def _get_casted_times(self, spell):
        if spell.name in self.casted_spells:
            return self.casted_spells[spell.name]
        else:
            return 0

    def _increase_casted_times(self, spell):
        if spell.name in self.casted_spells:
            if self.casted_spells[spell.name] < spell.max_usages:
                self.casted_spells[spell.name] += 1
                return True
            else:
                return False
        else:
            self.casted_spells[spell.name] = 1
            return True
        
    def _cast_dmg_spell(self):
        if self.spell_selected.spell_area_center.status == 0 or self.spell_selected.spell_area_center.status == 2:
            return self.map.get_attacked_entities(self.spell_selected.area_tiles, self.spell_selected.spell_dmg)
        else:
            return False
    
    def _cast_mov_spell(self):
        target_tile = self.spell_selected.spell_area_center
        if target_tile.status == 0:
            self.grid_pos = target_tile.grid_pos
            return True
        return False
    
    def cast_spell(self):
        casted = False
        if self.usable_ap >= self.spell_selected.ap_cost and self.spell_selected.spell_area_center is not None and self._get_casted_times(self.spell_selected) < self.spell_selected.max_usages:
            if self.spell_selected.type == "dmg":
                casted = self._cast_dmg_spell()
            elif self.spell_selected.type == "mov":
                casted = self._cast_mov_spell()
        
        if casted:
            self._update_ap(self.spell_selected.ap_cost)
            self._increase_casted_times(self.spell_selected)
        self.set_action('idle')
        
    def start_action(self):
        self.start_action_flag = not self.start_action_flag

    def draw_movement(self, surface):
            recons_path, _ = self.map.get_walking_path()
            if not self.steps:
                if recons_path:
                    if self.actions['idle']:
                        for node in recons_path:
                            surface.blit(
                                self.walking_hover,
                                node.rect.topleft
                            )
                    elif self.actions['moving']:
                        self.steps = recons_path
                        self.directions = _
                else:
                    return False
    
    def draw_spell_casting(self,surface):
        if self._get_casted_times(self.spell_selected) < self.spell_selected.max_usages:
            range_tiles = self.spell_selected.draw_spell_range(surface)
            hover_tile = self.map.get_hover_tile()
            if hover_tile and hover_tile in range_tiles:
                self.spell_selected.draw_spell_area(surface, hover_tile)
            else:
                self.spell_selected.spell_area_center = None
                self.spell_selected.area_tiles = None
             
    def draw(self, surface):
        if self.playing:
            if self.actions['idle'] or self.actions['moving']:
                self.draw_movement(surface)
            elif self.actions['pre_casting']:
                self.draw_spell_casting(surface)

        surface.blit(
            self.image,
            self.draw_pos
        )
        self.health_bar.draw(surface)
    
    def update(self):
        if self.playing:
            if self.actions['moving']:
                self.move()
            elif self.actions['spell_casting']:
                self.cast_spell()
        
            # UPDATING PLAYER TILE ON THE GRID AND DRAWING COMPONENTS
            self.animation.update()
            self.image = self.animation.img()
            self.update_tile()
            self._update_draw_pos()
            self._update_rect()