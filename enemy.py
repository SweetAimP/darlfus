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
                self.end_action()
                self.movement_clean_up()
    
    def knapsack_optimize_value(self, items, capacity):
        n = len(items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if items[i - 1].ap_cost <= w:
                    dp[i][w] = max(dp[i - 1][w], items[i - 1].spell_dmg + dp[i - 1][w - items[i - 1].ap_cost])
                else:
                    dp[i][w] = dp[i - 1][w]

        selected_items = []
        total_cost = 0
        total_value = dp[n][capacity]
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(items[i - 1])
                total_cost += items[i - 1].ap_cost
                w -= items[i - 1].ap_cost

        selected_items.reverse()
        return selected_items, total_cost, total_value

    def take_action(self):
        self.thinking = True
        capacity = self.ap
        items = []
        for spell in sorted(self.spells, key=lambda spell:spell.spell_dmg, reverse=True):
            for player in self.game.players_group.sprites():
                if distance_to(self.grid_pos, player.grid_pos) <= spell.range:
                    items.append(spell)
                    
        
        selected_items, total_cost, total_value = self.knapsack_optimize_value(items, capacity)
        print("Selected items:")
        for item in selected_items:
            print(f"Value: {item.spell_dmg}, Cost: {item.ap_cost}")
        print("Total cost:", total_cost)
        print("Total value:", total_value)


                
            

    def update(self):
        if self.playing:
            if not self.thinking:
                self.take_action()
            else:
                print("Thinking...")
        
    def end_turn(self):
        return super().end_turn()
