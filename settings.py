import pygame
import os
class Settings():
    def __init__(self):
        self.screen_width=288
        self.screen_height=512
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.datapath = 'sprites'
        #base
        self.imagebase=pygame.image.load(os.path.join(self.datapath,'base.bmp')).convert_alpha()
        self.base_width=336
        self.base_height=112

        self.bg_color=(0,0,0)
        # pipes
        self.move_step=1
        self.pipeimage=pygame.image.load(os.path.join(self.datapath,'pipe-green.bmp')).convert_alpha()
        self.uppipeimage=pygame.transform.rotate(self.pipeimage,180)
        self.pipe_width=52
        self.pipe_height=320
        self.number_pipes=4
        self.pipe_dist=(self.screen_width-self.number_pipes*self.pipe_width)\
                       /(self.number_pipes-1)
        self.disty=0.3*self.screen_height
        #bird
        self.imagemid =pygame.image.load(os.path.join(self.datapath,'redbird-midflap.bmp')).convert_alpha()
        self.imageup = pygame.image.load(os.path.join(self.datapath, 'redbird-upflap.bmp')).convert_alpha()
        self.imagedown = pygame.image.load(os.path.join(self.datapath, 'redbird-downflap.bmp')).convert_alpha()
        self.bird_x=0.3*self.screen_width
        self.bird_y=0.5*self.screen_height
        self.bird_move_dist=1.5
        self.bird_move_static=0.3  # higher more quick
        # global
        self.sleepseconds=0
        self.y=0
        #learning
        self.frequency=60