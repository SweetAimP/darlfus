import pygame as pg
from character import Character


class Enemy(Character):
    def __init__(self, game, pos, type, image, tag, *groups):
        super().__init__(pos, type, image, tag, *groups)
        self.game = game
        self.best_path_flag = False
        self.path = None
        self.target = None
        self.move_and_attack_flag = False
        self.attack_flag = False
        self.spell_used = None

    def start_turn(self):
        self.playing = True
        self.best_path_flag = False
        self.usable_mp = self.mp
        self.mp_used = 0
        self.ap_used = 0
        self.usable_ap = self.ap

    def get_best_paths(self):
        paths = []
        start = self.game.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]
        for target in self.game.players_group.sprites():
            end = self.game.map.grid[int(target.grid_pos[1])][int(target.grid_pos[0])]
            print(start.grid_pos,end.grid_pos)
            recons_path, _ = self.game.map.pathfinder.find_path(self.game.map.grid, start, end, self.tag)
            print(len(recons_path))
            paths.append([recons_path,target])
        shortest_path = min(paths, key=lambda path: len(path[0]))
        return shortest_path

    def take_action(self):
        if not self.best_path_flag:
            self.steps, self.target = self.get_best_paths()
            self.best_path_flag = True

            for spell in sorted(self.spells, key=lambda spell: spell.spell_dmg, reverse = True ):
                if spell.type == 'dmg':
                    self.spell_used = spell
                    if len(self.steps) <= spell.range:
                        self.attack_flag = True
                    elif len(self.steps) <= spell.range + self.usable_mp:
                        needed_steps = len(self.steps) - spell.range
                        if needed_steps <= self.usable_mp:
                            self.move_and_attack_flag =  True
                            break
        if self.attack_flag:
            self.attack(self.target, self.spell_used)
        elif self.move_and_attack_flag:
            self.move_and_attack(self.target, self.spell_used)

    def attack(self, target, spell):
        if self.usable_ap >= spell.ap_cost:
            target.take_damage(spell.spell_dmg)
            self.ap_used += spell.ap_cost
            self._update_ap()
        else:
            self.attack_flag = False
        

    def move_and_attack(self, target, spell):
        if self.current_step < len(self.steps):
            self.grid_pos = self.steps[self.current_step].grid_pos
            self.current_step += 1
            self.mp_used += 1
        else:
            self.clean_up()
            self._update_mp()
            print(self.usable_mp)
            self.attack(target, spell)

    def update(self):
        if self.playing:
            self.take_action()
            self._update_rect()
            self._update_draw_pos()
            
               
