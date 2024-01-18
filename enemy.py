import pygame as pg
from utils import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, game, tag, type, image, grid_pos, *groups):
        self.game  = game
        super().__init__(self.game.map, tag, type, image, grid_pos, *groups)

        # SPELL TYPE ARRAY
        self.dmg_spells = []
        self.mov_spells = []
        self._set_spells_array()
        self.min_dmg_ap_req = min(self.dmg_spells, key= lambda spell : spell.ap_cost).ap_cost
        self.min_mov_ap_req = min(self.mov_spells, key= lambda spell : spell.ap_cost).ap_cost

        # GAMEPLAY VARIABLES
        self.thinking = True
        self.casted = False
    
    def _set_spells_array(self):
        for spell in self.spells:
            if spell.type == 'dmg':
                self.dmg_spells.append(spell)
            elif spell.type == 'mov':
                self.mov_spells.append(spell)

    def _get_combo_actions(self, items, capacity):
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                for q in range(min(items[i - 1].max_usages, w // items[i - 1].ap_cost) + 1):
                    if q * items[i - 1].ap_cost <= w:
                        dp[i][w] = max(dp[i][w], q * items[i - 1].spell_dmg + dp[i - 1][w - q * items[i - 1].ap_cost])

        selected_items = []
        w = capacity
        used_quantities = {item: 0 for item in items}
        
        for i in range(n, 0, -1):
            for q in range(min(items[i - 1].max_usages, w // items[i - 1].ap_cost), 0, -1):
                while w >= q * items[i - 1].ap_cost and dp[i][w] == q * items[i - 1].spell_dmg + dp[i - 1][w - q * items[i - 1].ap_cost]:
                    selected_items.extend([items[i - 1]] * q)
                    w -= q * items[i - 1].ap_cost
                    used_quantities[items[i - 1]] += q

        selected_items.reverse()
        total_value = dp[n][capacity]
        
        return selected_items

    def _get_lowest_hp_target(self):
        return min(
                self.game.players_group.sprites(),
                key= lambda target: target.current_health
            )
    
    def _get_closest_target(self):
        return min(
                self.game.players_group.sprites(),
                key= lambda target: distance_to(self.grid_pos, target.grid_pos)
            )
    
    def _get_minimun_spell_range(self, combo):
        return min(
            combo,
            key= lambda spell: spell.range
        )
        
    def _move(self, target, steps):
        if steps > 0:
            target_tile = self.map.get_target_tile(target)
            recons_path, _ = self.map.get_walking_path(target_tile)
            if not self.steps:
                if recons_path:
                    self.steps = recons_path[:steps]
                    self.directions = _
                    return True
                else:
                    return False

    def _cast_spell(self, target, spell):
        target.take_damage(spell.spell_dmg)
        self._update_ap(spell.ap_cost)

    def take_action(self):
        # Getting the closest and lowest hp targets
        closest_target = self._get_closest_target()
        distance_closest_target = distance_to(self.grid_pos, closest_target.grid_pos)
        lowest_hp_target = self._get_lowest_hp_target()
        distance_lowest_hp_target = distance_to(self.grid_pos, lowest_hp_target.grid_pos)

        if self.usable_ap >= self.min_dmg_ap_req:
            best_dmg_combo = self._get_combo_actions(self.dmg_spells, self.usable_ap) # Conditioned if movement is needed (TODO)
            minimun_ranged_combo_action = self._get_minimun_spell_range(best_dmg_combo)
            final_target = lowest_hp_target if distance_lowest_hp_target < minimun_ranged_combo_action.range + self.usable_mp else closest_target
            distance_final_target = distance_to(self.grid_pos, final_target.grid_pos)
            if distance_to(self.grid_pos, final_target.grid_pos) <= minimun_ranged_combo_action.range:
                for spell in best_dmg_combo:
                    self._cast_spell(final_target, spell)
            else:
                steps = min(self.usable_mp, distance_final_target - minimun_ranged_combo_action.range)
                if self._move(final_target, steps):
                    self.set_action('moving')
                else:
                    self.end_turn()

        elif self.usable_mp > 0:
                farthest_tile = self.map.get_farthest_tile(closest_target)
                if self._move(farthest_tile, self.usable_mp):
                        self.set_action('moving')
        else:
            self.end_turn()

    def update(self):
        if self.playing:
            if self.actions['idle']:
                self.take_action()
            elif self.actions['moving']:
                self.move()

        # UPDATING PLAYER TILE ON THE GRID AND DRAWING COMPONENTS
        self.update_tile()
        self._update_draw_pos()
        self._update_rect()
      
    def end_turn(self):
        self.playing = False
        self.set_action('idle')
