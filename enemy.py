import pygame as pg
from utils import *
from entity import Entity

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
        self.final_target_distance = None
        self.count = 0
    
    def _set_spells_array(self):
        for spell in self.spells:
            if spell.type == 'dmg':
                self.dmg_spells.append(spell)
            elif spell.type == 'mov':
                self.mov_spells.append(spell)

    def _set_combo_actions(self, spells, spell_capacity):
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
        self.best_dmg_combo =  final_spells
        #return final_spells

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

    def _get_targets(self):
        closest_target = self._get_closest_target()
        lowest_hp_target = self._get_lowest_hp_target()
        return closest_target, lowest_hp_target
    
    def _set_attack_action(self):
        if self.spell_casting_index < len(self.best_dmg_combo):
            self.spell_selected = self.best_dmg_combo[self.spell_casting_index]
            self.spell_selected.draw_spell_range(self.game.screen)
            self.spell_selected.draw_spell_area(self.game.screen, self.final_target.tile)
            best_center = self._get_best_area()
            self.spell_selected._update_spell_area_center(best_center)
            self.set_action('attack', check_facing(best_center.grid_pos, self.grid_pos))
        else:
            self.casted = True
            self.set_action('idle', self.facing)

    def take_action(self):
        if [sprite for sprite in self.game.players_group.sprites() if not sprite.actions['death']]:
            closest_tg, lowest_tg = self._get_targets()
            closest_target_distance =  distance_to(self.grid_pos, closest_tg.grid_pos)
            lowest_hp_target_distance =  distance_to(self.grid_pos, lowest_tg.grid_pos)
            if not self.casted:
                self.final_target = lowest_tg if  lowest_hp_target_distance < closest_target_distance or lowest_hp_target_distance <= self.usable_mp else closest_tg
                self.final_target_distance = distance_to(self.grid_pos, self.final_target.grid_pos)
                if not self.best_dmg_combo :
                    self._set_combo_actions(self.spells, self.usable_ap)
                min_range = self._get_minimun_spell_range(self.best_dmg_combo)
                if self.final_target_distance > min_range.range:
                    if min_range.range + self.usable_mp >= self.final_target_distance:
                        steps = self.final_target_distance - min_range.range
                        self._move(self.final_target, steps)
                    else:
                        self.best_dmg_combo[self.spell_casting_index].draw_spell_range()
                        self._set_attack_action()
                else:
                   self._set_attack_action()
            elif not self.casted and self.best_dmg_combo:
                self._set_attack_action()
            elif self.casted:
                self.end_turn()

    def _get_best_area(self):
        best_center = None
        amount = 0
        new_area = None
        if self.spell_selected.area > 0:
            for tile in self.spell_selected.set_area_tiles(self.final_target.tile,'area'):
                if tile.type == 1:
                    new_area = self.spell_selected.set_area_tiles(tile,'area')
                else:
                    new_area = None
                if new_area != None:
                    temp_enemies = self.map.get_attacked_entities(new_area, 'npc')
                    if len(temp_enemies) > amount:
                        best_center = tile
                        amount = len(temp_enemies)
            return best_center
        return self.final_target.tile

    def attack(self):
        death = False
        death_player= None
        if self.animation.done:
            enemies_hitted = self.map.get_attacked_entities(self.spell_selected.set_area_tiles(self.spell_selected.spell_area_center, 'area'), 'npc')
            self._update_ap(self.spell_selected.ap_cost)
            self.spell_casting_index += 1
            self.set_action('idle', self.facing)
            for player in enemies_hitted:
                death = player.take_damage(self.spell_selected.spell_dmg)
                if death:
                    death_player = player
            if death_player == self.final_target:
                # self.spell_selected = None
                # self.best_dmg_combo = None
                # self.spell_casting_index = 0
                self.set_action('idle', self.facing)
        
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

    def draw(self, surface):
        if self.playing:
            surface.blit(
                self.walking_hover,
                self.tile.rect.topleft
            )
        super().draw(surface)

    def _set_action_cooldown(self):
        self.action_cooldown_time = pg.time.get_ticks()

    def _reset_spell_uses(self):
        for spell in self.spells:
            spell.remaining_uses = spell.max_usages

    def end_turn(self):
        self.playing = False
        self.casted = False
        self.spell_selected = None
        self.best_dmg_combo = None
        self.spell_casting_index = 0
        self.set_action('idle', self.facing)
    
    def start_turn(self):
        if super().start_turn():
            self._set_action_cooldown()
            self._reset_spell_uses()
