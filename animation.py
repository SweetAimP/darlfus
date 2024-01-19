
class Animation:
    def __init__(self, images, duration = 5, loop = True):
        self.animation_images = images
        self.animation_frame = 0
        self.duration = duration
        self.loop = loop
        self.done = False

    def copy(self):
        return Animation(self.animation_images, self.duration, self.loop)
    
    def update(self):
        if self.loop:
            self.animation_frame = (self.animation_frame + 1) % (self.duration * len(self.animation_images))
        else:
            self.animation_frame =  min(self.animation_frame + 1, self.duration * len(self.animation_images) - 1)
            if self.animation_frame >= self.duration * len(self.animation_images) - 1:
                self.done = True
            
    def img(self):
        return self.animation_images[int(self.animation_frame / self.duration)]