from utils import *
from tile import Tile
from pathfinder import PathFinder


class Map:
    def __init__(self, game):
        self.game = game
        self.grid_group = pg.sprite.Group()
        self.grid = None
        self.pathfinder = PathFinder()

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
                xs.append(Tile(
                        (x, y),
                        tile,
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
                        elif tile.status != 0 and self.game.current_player.spell_casting:
                            return tile
        return False
    
    def get_walking_path(self):
        end = self.get_hover_tile()
        if end and distance_to(self.game.current_player.grid_pos,end.grid_pos) <= self.game.current_player.usable_mp:
            start = self.game.map.get_current_player_tile(self.game.turn_order[self.game.current_player_index])
            if start != end:
                return self.game.map.pathfinder.find_path(self.game.map.grid, start, end, self.game.current_player.tag)
            else:
                return False, False
        else:
            return False, False

    def get_current_player_tile(self, player):
        return self.grid[int(player.grid_pos.y)][int(player.grid_pos.x)]
    
    def update(self):
        self.update_busy_tiles()
        self.update_neightbors()
    
    def draw(self):
        for row in self.grid:
            for tile in row:
                self.game.screen.blit(
                    tile.image,
                    tile.draw_pos
                )
