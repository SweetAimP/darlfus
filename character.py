from utils import *
from settings import *
from entities_settings import *
from spell import Spell
from healthbar import HealthBar

class Character(pg.sprite.Sprite):
    def __init__(self, pos, type, image, tag,*groups):
        super().__init__(*groups)
        self.grid_pos = pg.Vector2(pos)
        self.size = 32
        self.tag = tag
        self.entity_data = entities[type]
        self.max_health = self.entity_data['max_health']
        self.current_health = self.max_health
        self.initiative = self.entity_data['initiative']
        self.health_bar = HealthBar(self)
        # SPELLS
        self.spells = [ Spell(settings) for settings in self.entity_data["spells"]]

        # MOVEMENT AND ACTION POINTS
        self.mp = self.entity_data['mp']
        self.mp_used = 0
        self.usable_mp = self.mp - self.mp_used
        self.ap = self.entity_data['ap']
        self.ap_used = 0
        self.usable_ap = self.ap - self.ap_used
        

        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + OVERGRID_DRAW_OFFSET
        self.image = image #pg.image.load('assets/player/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.draw_pos)


        # GAME PLAY VARIABLES
        self.spell_casting = False
        self.playing = False
        self.moving = False 
        self.steps = []
        self.directions = []
        self.current_step = 0
        
    def get_instance(self):
        return self
    
    def clean_up(self):
        self.moving = False
        self.steps = []
        self.directions = []
        self.current_step = 0

    def start_turn(self):
        self.playing = True
        self.usable_mp = self.mp
        self.mp_used = 0
        self.ap_used = 0
        self.usable_ap = self.ap

    def _update_rect(self):
        self.rect.topleft = self.draw_pos

    def _update_draw_pos(self):
        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + OVERGRID_DRAW_OFFSET

    def _update_ap(self):
        self.usable_ap = self.ap - self.ap_used

    def _update_mp(self):
        self.usable_mp = self.mp - self.mp_used

    def move(self):
        if len(self.steps) > 0 and self.usable_mp > 0:
            self.grid_pos = self.steps[self.current_step].grid_pos
            if self.current_step + 1 < len(self.steps):
                self.current_step += 1
            else:
                self.mp_used += len(self.steps)
                self._update_mp()
                self.clean_up()

    def take_damage(self, dmg):
        if self.current_health > 0:
            self.current_health -= dmg
        else:
            print("Muere perro")

    def update(self):
        self.move()
        self._update_draw_pos()
        self._update_rect()
        self._update_ap()
        
    
    def draw(self, surface):
        surface.blit(
            self.image,
            self.draw_pos
        )
        