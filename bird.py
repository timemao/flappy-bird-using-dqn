class Bird():
    def __init__(self,ai_settings):
        self.screen=ai_settings.screen
        self.ai_settings=ai_settings
        self.image=self.ai_settings.imagemid
        self.ai_settings=ai_settings
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=self.ai_settings.bird_x,self.ai_settings.bird_y
        self.y=float(self.rect.y)
        self.x=float(self.rect.x)
        self.move_up=False
        self.move_down=False
    def update(self,stat):
        self.y += self.ai_settings.bird_move_static
        self.image=self.ai_settings.imagedown
        if self.move_up or stat.action=='up':
            self.y-=self.ai_settings.bird_move_dist
            self.image=self.ai_settings.imageup
        if self.move_down or stat.action=='down':
            self.y += self.ai_settings.bird_move_dist
            self.image=self.ai_settings.imagedown
        self.rect.y=self.y
    def blitme(self):
        self.screen.blit(self.image,(self.rect.x,self.rect.y))
