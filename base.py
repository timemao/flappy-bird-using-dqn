class Base():
    def __init__(self,ai_settings):
        self.screen=ai_settings.screen
        self.image=ai_settings.imagebase
        self.screen_rect = ai_settings.screen.get_rect()
        self.rect=self.image.get_rect()
        #center and bottom
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        #floating
        self.center=float(self.rect.centerx)
        self.y=float(self.rect.y)
    def update(self,ai_settings):
        if self.center<=(144-(168-144)):
            self.center=(144+(168-144))
        self.center-=ai_settings.move_step
        self.rect.centerx=self.center
    def blitme(self):
        self.screen.blit(self.image,self.rect)