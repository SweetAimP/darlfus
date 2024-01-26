import pygame as pg
from utils import *
from entity import Entity
from itertools import product


class Enemy(Entity):
    def __init__(self, game, tag, type, grid_pos, *groups):
        super().__init__(game, tag, type, grid_pos, *groups)
        # SPELL TYPE ARRAY
        self.dmg_spells = []
        self.mov_spells = []
        self._set_spells_array()
        self.min_dmg_ap_req = 99 if len(self.dmg_spells) == 0 else min(self.dmg_spells, key= lambda spell : spell.ap_cost).ap_cost
        self.min_mov_ap_req = 99 if len(self.mov_spells) == 0 else min(self.mov_spells, key= lambda spell : spell.ap_cost).ap_cost

        # GAMEPLAY VARIABLES
        self.thinking = True
        self.casted = False
        self.action_cooldown = 2000
        self.action_cooldown_time = None
        self.best_dmg_combo = None
        self.spell_casting_index = 0
        self.final_target = None
    
    def _set_spells_array(self):
        for spell in self.spells:
            if spell.type == 'dmg':
                self.dmg_spells.append(spell)
            elif spell.type == 'mov':
                self.mov_spells.append(spell)

    def _get_combo_actions(self, spells, spell_capacity):
        memo = {}  # Dictionary to store already computed results
        def dp(current_spell, remaining_capacity):
            if current_spell < 0 or remaining_capacity == 0:
                return 0, []

            if (current_spell, remaining_capacity) in memo:
                return memo[(current_spell, remaining_capacity)]

            max_damage = 0
            best_combo = []

            # Try using the current spell
            for uses in range(min(spells[current_spell].remaining_uses, remaining_capacity // spells[current_spell].ap_cost) + 1):
                total_damage, remaining_combos = dp(current_spell - 1, remaining_capacity - uses * spells[current_spell].ap_cost)
                total_damage += uses * spells[current_spell].spell_dmg

                if total_damage > max_damage:
                    max_damage = total_damage
                    best_combo = remaining_combos + [(spells[current_spell], uses)]

            memo[(current_spell, remaining_capacity)] = max_damage, best_combo
            return total_damage, best_combo

        total_damage, selected_spells = dp(len(spells) - 1, spell_capacity)
        final_spells = []
        for spell, uses in selected_spells:
            for _ in range(uses):
                final_spells.append(spell)
        return final_spells

    def _get_lowest_hp_target(self):
        return min(
                [sprite for sprite in self.game.players_group.sprites() if not sprite.actions['death']],
                key= lambda target: target.current_health
            )
    
    def _get_closest_target(self):
        return min(
                [sprite for sprite in self.game.players_group.sprites() if not sprite.actions['death']],
                key= lambda target: distance_to(self.grid_pos, target.grid_pos)
            )
    
    def _get_minimun_spell_range(self, combo):
        return min(
            combo,
            key= lambda spell: spell.range
        )
        
    def _move(self, target, steps):
        if steps > 0:
            target_tile = target
            self.set_action('walk', self.facing)
            if hasattr(target, 'tile'):
                target_tile = self.map.get_target_tile(target)
            recons_path, directions = self.map.get_walking_path(target_tile)
            if not self.steps:
                if recons_path:
                    self.steps = recons_path[:steps]
                    self.directions = directions
                    return True
                else:
                    return False
        else:
            return False
        
    def _update_spell(self, spell, area_center):
        spell._update_spell_area_center(area_center)
        spell.area_tiles = spell.set_area_tiles(spell.spell_area_center, 'area')

    def _cast_spell(self, target, spell):
        if spell.area > 0:
            center = self._get_best_area_tile(spell)
        else:
            center = target.tile

        self._update_spell(spell, center)
        enemies_hitted = self.map.get_attacked_entities(spell.area_tiles, self.tag)
        self._update_ap(spell.ap_cost)
        spell.remaining_uses -= 1
        keep_attacking = False
        for enemy in enemies_hitted:
            if enemy.take_damage(spell.spell_dmg):
                if enemy.tile == spell.spell_area_center:
                    keep_attacking = False
            else:
                keep_attacking = True

        return keep_attacking
    
    def take_action(self):
        # Getting the closest and lowest hp targets
        players = [sprite for sprite in self.game.players_group.sprites() if not sprite.actions['death']]
        if players:
            closest_target =  self._get_closest_target()
            lowest_hp_target =  self._get_closest_target()
            if self.usable_ap >= self.min_dmg_ap_req and not self.casted:
                self.best_dmg_combo = self._get_combo_actions(self.spells, self.usable_ap)
                min_range_spell = self._get_minimun_spell_range(self.best_dmg_combo)
                distance_closest_target = distance_to(self.grid_pos, closest_target.grid_pos)
                distance_lowest_hp_target = distance_to(self.grid_pos, lowest_hp_target.grid_pos)
                self.final_target = closest_target if distance_closest_target < distance_lowest_hp_target else lowest_hp_target
                distance_final_target = distance_to(self.grid_pos, self.final_target.grid_pos)
                best_area_center = None
                if min_range_spell.area > 0:
                    best_area_center = self._get_best_area_tile(min_range_spell)
                if distance_final_target <= min_range_spell.range:
                    self.set_action("attack" , check_facing(self.final_target.grid_pos, self.grid_pos))
                else:
                    to_go = best_area_center if best_area_center is not None else self.final_target
                    steps = min(self.usable_mp, distance_final_target - min_range_spell.range)
                    if not self._move(to_go, steps):
                        self.end_turn()
            elif self.usable_mp > 0:
                    farthest_tile = self.map.get_farthest_tile(closest_target)
                    if not self._move(farthest_tile, self.usable_mp):
                        self.end_turn()
            else:
                self.end_turn()

            
            
            


    def draw(self, surface):
        if self.playing:
            surface.blit(
                self.walking_hover,
                self.tile.rect.topleft
            )
        super().draw(surface)

    def _get_best_area_tile(self, spell):
        # TEST
        final_target_area = spell.set_area_tiles(self.final_target.tile, 'area')
        entities = 1
        best_area_center = self.final_target.tile
        distance_center_tile = distance_to(self.grid_pos, best_area_center.grid_pos)
        for tile in final_target_area:
            new_area_tiles = spell.set_area_tiles(tile, 'area')
            attacked_entitties =  len(self.map.get_attacked_entities(new_area_tiles,self.tag))
            new_distance = distance_to(self.grid_pos, tile.grid_pos)
            if attacked_entitties > entities and new_distance < distance_center_tile :
                entities = attacked_entitties
                best_area_center = tile
                distance_center_tile = new_distance
                
        
        area = spell.draw_spell_area(self.game.screen,best_area_center)
        return best_area_center

    def attack(self):
        if self.spell_casting_index < len(self.best_dmg_combo):
            if self.animation.done:
                test = self._cast_spell(self.final_target, self.best_dmg_combo[self.spell_casting_index])
                if test:
                    self.set_action("idle", self.facing)
                    self.animation.done = False
                    self.spell_casting_index += 1
                else:
                    self.set_action("idle", self.facing)
        else:
            self.spell_casting_index = 0
            self.set_action("idle", self.facing)

            
                

    def update(self):
        if self.playing:
            if pg.time.get_ticks() - self.action_cooldown_time >=  self.action_cooldown:
                if self.actions['idle']:
                    self.take_action()
                elif self.actions['walk']:
                    self.move()
                elif self.actions["attack"]:
                    self.attack()
        if self.actions['death']:
            self.death()

        # UPDATING PLAYER TILE ON THE GRID AND DRAWING COMPONENTS
        self.animation.update()
        self.image = self.animation.img()
        self.update_tile()
        self._update_draw_pos()
        self._update_rect()

    def _set_action_cooldown(self):
        self.action_cooldown_time = pg.time.get_ticks()

    def _reset_spell_uses(self):
        for spell in self.spells:
            spell.remaining_uses = spell.max_usages

    def end_turn(self):
        self.playing = False
        self.casted = False
        self.set_action('idle', self.facing)
    
    def start_turn(self):
        if super().start_turn():
            self._set_action_cooldown()
            self._reset_spell_uses()
