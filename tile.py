from utils import *
from settings import *

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, type, *group):
        super().__init__(*group)
        self.grid_pos = pg.Vector2(pos)
        self.type = type # Type determines if the tile is walkable or not
        self.status = self.set_status() # Status indicates if the Tile is Free(0) or Taken(1) ** can be modified from the game cycle
        self.walkable = self.set_walkable() # indiacates if can be walked on or not
        self.neighbors = []
        self.size = 32
        self.tiles_types = ['assets/tiles/void.png','assets/tiles/basic_tile.png']
        self.draw_pos = cartisian_to_iso(self.grid_pos, self.size) + GRID_DRAW_OFFSET
        self.image = pg.image.load(self.tiles_types[self.type]).convert_alpha()
        self.hover_img = pg.image.load("assets/mouse/hover.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=self.draw_pos)
    
    def set_status(self):
        if self.type == 1:
            return 0
        else:
            return 1
        
    def set_walkable(self):
        if self.status == 0:
            self.walkable = True
        else:
            self.walkable = False
            
    def get_pos(self):
        return self.grid_pos
    
    def get_neighbors(self):
        return self.neighbors
    
    def __lt__(self, other): #need for the revision of less than during the neighborm score asignation
        return False
                