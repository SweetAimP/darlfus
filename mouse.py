import pygame as pg
import sys

class Mouse:
    def __init__(self, game):
        self.game = game

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                current_player = self.game.current_player.get_instance()
                if current_player.tag  == 'player':
                    # Access all the event hanlders from entities
                    if self.game.end_turn_rect.collidepoint(self.get_pos()):
                        current_player.end_turn()
                    elif self.game.get_spell_selected(self.get_pos()):  
                        current_player.moving = False
                        current_player.spell_casting = True
                    elif current_player.spell_casting:
                        current_player.spell_casting = False
                        current_player.moving = True
                    elif current_player.moving:
                        current_player.on_click()
                        
    def get_pos(self):
        return pg.mouse.get_pos()
            
    def get_attacked_entities(self): # move responsability to the map if dmg map if mov player/ntity
        if self.game.current_player.spells[self.spell_casting_index].type == "dmg":
            for entity in self.game.turn_order:
                    if entity != self.game.current_player:
                        if self.game.map.grid[int(entity.grid_pos[1])][int(entity.grid_pos[0])] in self.casting_impact_tiles:
                                print("pepe")
                                entity.take_damage(self.game.current_player.spells[self.spell_casting_index].spell_dmg)
            return True
        elif self.game.current_player.spells[self.spell_casting_index].type == "mov":
            target_tile = list(self.casting_impact_tiles)[0]
            if target_tile.status == 0:
                self.game.current_player.grid_pos = target_tile.grid_pos
                return True
            return False
         