import pygame as pg

class HealthBar:
    def __init__(self, owner):
        self.owner = owner
        self.width = 60
        self.height = 5
    
    def update(self):
        pass

    def draw(self, surface):
        rect_pos = self.owner.rect.topleft
        health_ratio = self.owner.current_health / self.owner.max_health
        health_bar_base_rect = pg.Rect(rect_pos[0] - 16, rect_pos[1] - 10, self.width, self.height)
        health_bar_rect = pg.Rect(rect_pos[0] - 16, rect_pos[1] - 10, int(health_ratio * self.width), self.height)
        pg.draw.rect(
            surface,
            'red',
            health_bar_base_rect
        )
        pg.draw.rect(
            surface,
            'green',
            health_bar_rect
        )

        
