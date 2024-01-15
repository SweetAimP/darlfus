from entity import Entity
from utils import *

class Player(Entity):
    def __init__(self, map, tag, type, image, grid_pos, *groups):
        super().__init__(map, tag, type, image, grid_pos, *groups)
        self.map = map

        # FLAGS
        self.spell_casting = False
        self.spell_selected = None
        self.clicked = False
    
    def end_turn(self):
        self.playing = False
        self.spell_casting = False
        self.moving = False
        self.clicked = False
        self.movement_clean_up()
        
    def move(self):
        if len(self.steps) > 0 and self.usable_mp > 0:
            self.grid_pos = self.steps[self.current_step].grid_pos
            if self.current_step + 1 < len(self.steps):
                self.current_step += 1
            else:
                self.mp_used += len(self.steps)
                self._update_mp()
                self.on_click()
                self.movement_clean_up()

    def on_click(self):
        self.clicked = not self.clicked

    def draw_movement(self, surface):
            recons_path, _ = self.map.get_walking_path()
            if not self.steps:
                if recons_path:
                    for node in recons_path:
                        surface.blit(
                            node.hover_img,
                            node.rect.topleft
                        )
                    if self.clicked:
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
        if self.clicked:
            self.move()
        self._update_draw_pos()
        self._update_rect()
        self._update_ap()