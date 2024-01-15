from entity import Entity

class Player(Entity):
    def __init__(self, game, tag, type, image, grid_pos, *groups):
        super().__init__(game, tag, type, image, grid_pos, *groups)

        # FLAGS
        self.spell_casting = False
        
    def move(self):
        if len(self.steps) > 0 and self.usable_mp > 0:
            self.grid_pos = self.steps[self.current_step].grid_pos
            if self.current_step + 1 < len(self.steps):
                self.current_step += 1
            else:
                self.mp_used += len(self.steps)
                self._update_mp()
                self.clean_up()

    def update(self):
        self.move()
        self._update_draw_pos()
        self._update_rect()
        self._update_ap()