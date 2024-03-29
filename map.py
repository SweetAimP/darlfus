from utils import *
from tile import Tile
from pathfinder import PathFinder
from settings import TILE_IMAGES


class Map:
    def __init__(self, game):
        self.game = game
        self.grid_group = pg.sprite.Group()
        self.grid = None
        self.pathfinder = PathFinder()
        self.tile_images = [pg.image.load(t).convert_alpha() for t in sorted(TILE_IMAGES)]

    def update_busy_tiles(self):
        for row in self.grid:
            for tile in row:
                if tile.type == 1:
                    for entity in self.game.entity_group.sprites():
                        if hasattr(entity, 'grid_pos') and tile.grid_pos == entity.grid_pos:
                            tile.status = 2
                            break
                        else:
                            tile.status = 0
                tile.set_walkable()
                
    def update_neightbors(self):
        col_len = len(self.grid)
        for y, row in enumerate(self.grid): # arreglo con las Tiles de x
            row_len = len(row) # Cantidad de X por fila(row)
            for x, tile in enumerate(row): # Tiles dentro del arreglo
                    # Validando vecinos en la horizontal
                    tile.neighbors = []
                    if x > 0: # revisar a la izquierda
                        tile.neighbors.append(self.grid[y][x - 1])
                    if x >= 0 and x + 1 <= row_len - 1: # revisar vecinos de la derecha
                        tile.neighbors.append(self.grid[y][x + 1])
                    # Validando vecinos en la vertical
                            
                    if y > 0: # revisar arriba
                        tile.neighbors.append(self.grid[y - 1][x])
                    if y >= 0 and y + 1 <= col_len - 1: # revisar abajo
                        tile.neighbors.append(self.grid[y + 1][x])

    def make_grid(self, map_file):
        grid = []
        map_data = read_map_file(map_file)
        for y, row in enumerate(map_data):
            xs = []
            for x, tile in enumerate(row):
                tile_img = None
                if tile == 1:
                    tile_img = self.tile_images[0]
                elif tile == 2:
                    tile_img = self.tile_images[1]
                else:
                    tile_img = self.tile_images[2]
                xs.append(Tile(
                        (x, y),
                        tile,
                        tile_img,
                        self.grid_group
                    )
                )
            grid.append(xs)
        self.grid = grid
        self.update_busy_tiles()
        self.update_neightbors()
    
    def get_hover_tile(self):
        point = self.game.mouse.get_pos()
        for row in self.grid:
            for tile in row:
                    if tile.rect.collidepoint(point) and tile.draw_pos.distance_to(point) < 20:
                        if tile.status == 0:
                            return tile
                        elif tile.status != 0 and self.game.current_player.actions['pre_cast']:
                            return tile
        return False
    
    def _call_pathfinder(self,start, end, current_player):
        if start != end:
            return self.game.map.pathfinder.find_path(self.game.map.grid, start, end, current_player)
        else:
            return False, False
         
    def get_walking_path(self, end = False):
        end = self.get_hover_tile() if not end else end
        start = self.game.current_player.tile

        if self.game.current_player.tag == 'player' and end and distance_to(self.game.current_player.grid_pos,end.grid_pos) <= self.game.current_player.usable_mp:
            return self._call_pathfinder(start,end, self.game.current_player)
        elif self.game.current_player.tag == 'npc':
            return self._call_pathfinder(start,end, self.game.current_player)
        else:
            return False, False
    
    def get_attacked_entities(self, cast_area, caster):
        entities_hitted = []
        if caster == 'player':
            for enemy in self.game.enemies_group.sprites():
                if enemy.tile in cast_area:
                    entities_hitted.append(enemy)
        elif caster == 'npc':
            for player in self.game.players_group.sprites():
                if player.tile in cast_area:
                    entities_hitted.append(player)
        return entities_hitted
    
    def get_farthest_tile(self, target):
        farthest_tile = None
        max_distance = 0

        for row in self.grid:
            for tile in row:
                distance = distance_to(target.grid_pos, tile.grid_pos)
                if distance > max_distance:
                    max_distance = distance
                    farthest_tile = tile
        
        return farthest_tile

    def get_target_tile(self, target):
        if hasattr(target, 'tile'):
            return target.tile
        elif isinstance(target, pg.Vector2):
            return self.grid[int(target[1])][int(target[0])]
        elif isinstance(target, Tile):
            return target
        else:
            return False

    def update(self):
        self.update_busy_tiles()
        self.update_neightbors()
    
    def draw(self):
        for sprite in self.grid_group.sprites():
            self.game.screen.blit(
                sprite.image,
                sprite.draw_pos
            )
