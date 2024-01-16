import pygame as pg
from utils import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, game, tag, type, image, grid_pos, *groups):
        self.game  = game
        super().__init__(self.game.map, tag, type, image, grid_pos, *groups)
        self.thinking = False
    

    def move(self):
        if len(self.steps) > 0 and self.usable_mp > 0:
            self.grid_pos = self.steps[self.current_step].grid_pos
            if self.current_step + 1 < len(self.steps):
                self.current_step += 1
            else:
                mp_used = len(self.steps)
                self._update_mp(mp_used)
                self.movement_clean_up()
                self.end_turn()
    
    def travelers_bag(self, items, capacity):
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
        
        return selected_items, total_value

    def take_action(self):
        self.thinking = True
        # capacity = self.ap
        # spells = []
        # target = None
        # for spell in self.spells:
        #     for player in self.game.players_group.sprites():
        #         if distance_to(self.grid_pos, player.grid_pos) <= spell.range:
        #             spells.append(spell)
        #             if target != player:
        #                 target = player
        
        # selected_items, total_value = self.travelers_bag(spells, capacity)
        for spell in self.spells:
            for player in self.game.players_group.sprites():
                distance = distance_to(self.grid_pos, player.grid_pos)
                if distance > spell.range:
                    steps = int(distance - spell.range)
                    recons_path, _ = self.map.get_walking_path(player.tile)
                    if not self.steps:
                        if recons_path:
                            for node in recons_path[:steps]:
                                self.game.screen.blit(
                                    node.hover_img,
                                    node.rect.topleft
                                )
                            self.steps = recons_path[:steps]
                            self.directions = _

        self.moving = True   

    def update(self):
        self.update_tile()
        if self.playing:
            if not self.thinking:
                self.take_action()
            elif self.moving:
                self.move()
        self._update_draw_pos()
        self._update_rect()

        
    def end_turn(self):
        self.thinking = not self.thinking
        self.playing = not self.playing
