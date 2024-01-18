import pygame as pg
from utils import distance_to
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

                    elif self.game.get_spell_selected(self.get_pos()):  # Control the current player state (Moving / Spell-casting)
                        current_player.set_action('pre_casting')

                    elif current_player.actions['pre_casting']:
                        current_player.set_action('spell_casting')
                        
                    elif current_player.actions['idle']:
                        hover_tile = self.game.map.get_hover_tile()
                        if hover_tile and distance_to(current_player.grid_pos,hover_tile.grid_pos) <= current_player.usable_mp:
                            current_player.set_action('moving')

                        
    def get_pos(self):
        return pg.mouse.get_pos()
        
         