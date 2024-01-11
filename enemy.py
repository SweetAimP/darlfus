import pygame as pg
from character import Character


class Enemy(Character):
    def __init__(self, game, pos, type, image, tag, *groups):
        super().__init__(pos, type, image, tag, *groups)
        self.game = game
        self.best_path_flag = False
        self.paths = None
      
    def get_best_paths(self):
        paths = []
        start = self.game.map.grid[int(self.grid_pos[1])][int(self.grid_pos[0])]
        for target in self.game.players_group.sprites():
            end = self.game.map.grid[int(target.grid_pos[1])][int(target.grid_pos[0])]
            recons_path, _ = self.game.map.pathfinder.find_path(self.game.map.grid, start, end, self.usable_mp, self.tag)
            paths.append(recons_path)
        shortest_path = min(paths, key=lambda path: len(path))
        return shortest_path

    def take_action(self):
        if not self.best_path_flag:
            self.path = self.get_best_paths()
            self.best_path_flag = True

        for entity in self.game.players_group.sprites():
            if entity.tag == 'player':
                for spell in sorted(self.spells, key=lambda spell: spell.spell_dmg, reverse = True ):
                    if spell.type == 'dmg':
                        if len(self.path) <= spell.range:
                            print("En alcance")
                        elif len(self.path) <= spell.range + self.usable_mp:
                            print(f"En alcance si me muevo {len(self.path) - spell.range} casillas")
        self.best_path_flag= False




    def update(self):
        if self.playing:
            self.take_action()
            # self.__update_draw_pos()
            # self.__update_rect()
            # self.__update_ap()
               
