from pygame.sprite import Sprite
import random
class Pipe(Sprite):
    def __init__(self,ai_settings):
        super(Pipe,self).__init__()
        self.ai_settings=ai_settings
        self.screen=ai_settings.screen
        self.image=self.ai_settings.pipeimage
        self.rect=self.image.get_rect()
        self.x=float(self.rect.x)
    def update(self):
        self.x-=self.ai_settings.move_step
        self.rect.x=self.x
class upPipe(Sprite):
    def __init__(self,ai_settings):
        super(upPipe,self).__init__()
        self.ai_settings=ai_settings
        self.image=self.ai_settings.uppipeimage
        self.screen=ai_settings.screen
        self.rect=self.image.get_rect()
        self.y=-(random.randrange(100,220))
        self.rect.y=self.y
        self.x = float(self.rect.x)
    def update(self):
        self.x-=self.ai_settings.move_step
        self.rect.x=self.x