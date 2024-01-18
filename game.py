import time
from utils import *
from settings import *
from map import Map
from entity_group import EntityGroup
from player import Player
from enemy import Enemy
from mouse import Mouse
from spell_menu import Spell_menu

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_SIZE['width'],SCREEN_SIZE['height']))
        self.clock = pg.time.Clock()
        self.turn_font = pg.Font(None, 40)
        self.spell_font = pg.Font(None, 40)
        self.spells_menu = Spell_menu()
        
        # GROUPS
        self.players_group = pg.sprite.Group()
        self.enemies_group = pg.sprite.Group()
        self.entity_group = EntityGroup()

        # MAP
        self.map = Map(self._get_instance())
        self.draw_base_grid()
        self.map.make_grid('map.txt')
        
        # PLAYERS
        Player(self, 'player', 'archer',pg.image.load(ENTITIES_IMGS[0]).convert_alpha(),(5,10), self.entity_group ,self.players_group)
        Player(self, 'player', 'archer',pg.image.load(ENTITIES_IMGS[0]).convert_alpha(),(9,7), self.entity_group ,self.players_group)
        # ENEMIES
        Enemy(self._get_instance(), 'npc', 'archer',pg.image.load(ENTITIES_IMGS[1]).convert_alpha(),(19,6), self.entity_group ,self.enemies_group)
        Enemy(self._get_instance(), 'npc', 'archer',pg.image.load(ENTITIES_IMGS[1]).convert_alpha(),(3,6), self.entity_group ,self.enemies_group)

        # CONTROLS
        self.mouse = Mouse(self._get_instance())
       
        # GAMEPLAY VARIABLES
        self.turn_order = sorted( self.entity_group, key=lambda entity: entity.initiative, reverse=True)
        self.turn_start_time = None
        self.current_player_index = 0
        self.turn_time_limit = 40
        self.current_player = self.get_current_player()

        # INITIALIZATON FORCED
        self.turn_order[0].start_turn()
        self.spells_menu.create_spell_rects(len(self.current_player.spells))
        self.map.grid_group.update(self.entity_group)
             
    def _get_instance(self):
        return self
    
    def get_current_player(self):
        return self.turn_order[self.current_player_index].get_instance()

    def draw_base_grid(self):
        gap = SCREEN_SIZE['width']//20
        for i in range(20):
            pg.draw.line(self.screen,'grey',(0,i*gap), (SCREEN_SIZE['width'],i*gap))
        for j in range(20):
            pg.draw.line(self.screen,'grey',(j*gap,0), (j*gap,SCREEN_SIZE['width']))
    
    def switch_turn(self):
        self.current_player.end_turn()
        self.current_player_index = (self.current_player_index + 1) % len(self.turn_order)
        self.current_player = self.get_current_player()
        self.spells_menu.create_spell_rects(len(self.current_player.spells))
        self.current_player.start_turn()
        self.turn_start_time = time.time()
        
    def end_turn_btn(self):
        button_rect = pg.Rect(0, SCREEN_SIZE['height'] - 50, SCREEN_SIZE['width'], 50)
        pg.draw.rect(self.screen, 'white', button_rect)

        text_surface = self.turn_font.render("End Turn", True, 'orange')
        self.end_turn_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, self.end_turn_rect)
    
    def __check_turn_timer(self, elapsed_time):
        if elapsed_time > self.turn_time_limit:
            self.switch_turn()

    def _draw_turn_timer(self,start_time):
        elapsed_time = int(time.time() - start_time)
        text = self.turn_font.render(str(self.turn_time_limit - elapsed_time), True, 'orange')
        text_rect =  text.get_rect(topleft = (SCREEN_SIZE['width']*0.025,SCREEN_SIZE['height']*0.025))
        self.screen.blit(
            text,text_rect
        )
        self.__check_turn_timer(elapsed_time)

    def get_spell_selected(self, mouse_pos):
        for spell_index, spell_rect in enumerate(self.spells_menu.spell_rects):
            if spell_rect.collidepoint(mouse_pos):
                self.current_player.spell_selected = self.current_player.spells[spell_index]
                if self.current_player.usable_ap >= self.current_player.spell_selected.ap_cost:
                    return True
        return False
    
    def Kill_entity(self, entity):
        index = self.turn_order.index(entity)
        self.turn_order.pop(index)
        entity.kill()
        
    def run(self):
        self.turn_start_time = time.time()
        while True:
            # Clearing the screen
            self.screen.fill('black')
            self.draw_base_grid()
            self.spells_menu.draw_spell_menu(self.screen, self.spell_font)
            
            # Listening for mouse events (click)
            self.mouse.check_events()

            if not self.current_player.playing:
                self.switch_turn()
            
            # DRAWING MAP TILES
            self.map.update()
            self.map.draw()

            # ENTITIES
            self.entity_group.update()
            self.entity_group.draw(self.screen)
            
            # TURN TIMER    
            self.end_turn_btn()
            self._draw_turn_timer(self.turn_start_time)

            # Updating the main screen
            pg.display.flip()
            self.clock.tick(FPS)

Game().run()