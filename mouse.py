import pygame as pg
import sys

class Mouse:
    def __init__(self, game):
        self.game = game
        self.image =  pg.image.load('assets/mouse/hover.png').convert_alpha()
        self.clicked = False
        self.spell_casting = False
        self.spell_casting_index = None
        self.casting_impact_tiles = None

    def clean_up(self):
        self.clicked = False
        self.spell_casting =  False
        self.spell_casting_index = None


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and not self.clicked:
                current_player = self.game.current_player.get_instance()
                # Access all the event hanlders from entities
                if self.game.end_turn_rect.collidepoint(self.get_pos()): # CHECK FOR END TURN INPUT
                    current_player.playing = False
                    self.clean_up()
                elif self.get_spell_selected():  
                    self.spell_casting =  True
                    current_player.spell_casting = True
                elif self.spell_casting:
                    if self.get_attacked_entities():
                        self.game.current_player.ap_used += self.game.current_player.spells[self.spell_casting_index].ap_cost
                        self.clean_up()
                elif not self.spell_casting:
                    recons_path, directions = self.get_walking_path(self.game.current_player.usable_mp)
                    if recons_path:  # CHECK FOR MOVEMENT INPUT
                        current_player.moving = True
                        current_player.steps =  recons_path
                        current_player.directions = directions
                
                

    def get_spell_selected(self):
        for spell_index, spell_rect in enumerate(self.game.spells_menu.spell_rects):
            if spell_rect.collidepoint(self.get_pos()) and self.game.current_player.usable_ap >= self.game.current_player.spells[spell_index].ap_cost: # SPELL CASTING
                self.spell_casting_index = spell_index
                return True
        return False

    def click(self):
        return pg.mouse.get_pos()
    
    def get_pos(self):
        return pg.mouse.get_pos()
    
    def get_walking_path(self,player_mp):
        end = self.game.map.get_hover_tile(self.get_pos())
        if end:
            start = self.game.map.get_current_player_tile(self.game.turn_order[self.game.current_player_index])
            if start != end:
                return self.game.map.pathfinder.find_path(self.game.map.grid, start, end, player_mp, self.game.current_player.tag)
            else:
                return False, False
        else:
            return False, False
        
    def draw(self):
        if not self.spell_casting:
            recons_path, _ = self.get_walking_path(self.game.current_player.usable_mp)   
            if recons_path:
                for node in recons_path:
                    self.game.screen.blit(
                        self.image,
                        node.rect.topleft
                    )
        elif self.spell_casting:
            point = self.get_pos()
            range_tiles = self.game.current_player.spells[self.spell_casting_index].draw_range(self.game.map.grid[int(self.game.current_player.grid_pos[1])][int(self.game.current_player.grid_pos[0])])
            for tile in range_tiles:
                if tile.rect.collidepoint(point) and tile.draw_pos.distance_to(point) < 20:
                    area_tiles = self.game.current_player.spells[self.spell_casting_index].draw_spell_area(tile)
                    self.casting_impact_tiles = area_tiles
                    break
            
    def get_attacked_entities(self):
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

    def update(self):
        if not self.game.current_player.moving and not self.game.current_player.spell_casting:
            self.clicked = False