import sys
import pygame
from base import Base
from pipe import upPipe
from pipe import Pipe
import random
import cv2
def check_event(bird,stat):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN:
                bird.move_down=True
                stat.action='down'
            if event.key==pygame.K_UP:
                bird.move_up=True
                stat.action='up'
        elif event.type==pygame.KEYUP:
            bird.move_down=False
            bird.move_up=False
            stat.action=''
def update_screen(ai_settings,base,pipes,uppipes,bird):
    ai_settings.screen.fill(ai_settings.bg_color)
    pipes.draw(ai_settings.screen)
    uppipes.draw(ai_settings.screen)
    base.blitme()
    bird.blitme()
    pygame.display.flip()
def create_pipes(ai_settings,pipes,uppipes):
    number_pipes=ai_settings.number_pipes
    uppipes_y=[0,0,0,0]
    for number_pipe in range(number_pipes):
        create_uppipe(ai_settings, uppipes, number_pipe,uppipes_y)
        create_pipe(ai_settings,pipes,number_pipe,uppipes_y)
def create_uppipe(ai_settings,uppipes,number_pipe,uppipes_y):
    uppipe = upPipe(ai_settings)
    uppipe.x=ai_settings.screen_width+ai_settings.pipe_width/2\
                    +number_pipe*(ai_settings.screen_width/(ai_settings.number_pipes-2))
    uppipe.rect.x =uppipe.x
    uppipes.add(uppipe)
    uppipes_y[number_pipe]=float(uppipe.rect.y)
def create_pipe(ai_settings,pipes,number_pipe,uppipes_y):
    pipe = Pipe(ai_settings)
    pipe.x=ai_settings.screen_width+ai_settings.pipe_width/2\
                    +number_pipe*(ai_settings.screen_width /(ai_settings.number_pipes-2))
    pipe.rect.x =pipe.x
    pipe.rect.y=uppipes_y[number_pipe]+ai_settings.pipe_height+ai_settings.disty
    pipes.add(pipe)
def update_pipes(ai_settings,pipes,uppipes):
    ai_settings.y = 0
    for uppipe in uppipes:
        if uppipe.x+ai_settings.pipe_width<=0:
            ai_settings.y= -(random.randrange(100, 220))

            uppipe.x=524
            uppipe.y =ai_settings.y
            uppipe.rect.y = uppipe.y
            uppipe.rect.x=uppipe.x
            for pipe in pipes:
                if pipe.x + ai_settings.pipe_width <= 0:
                    pipe.x = 524
                    pipe.rect.x=pipe.x
                    pipe.y=ai_settings.y+ai_settings.pipe_height+ai_settings.disty
                    pipe.rect.y=pipe.y
    pipes.update()
    uppipes.update()
def check_crash(bird,pipes,uppipes,base,stat):
    if bird.rect.y+bird.rect.height>=base.y or bird.rect.y<=0:
        stat.action_reward = -1
        stat.game_active = False
    elif pygame.sprite.spritecollideany(bird,pipes) or pygame.sprite.spritecollideany(bird,uppipes):
        stat.action_reward = -1
        stat.game_active = False
def score(bird,pipes,stat):
    for pipe in pipes:
        if pipe.x+pipe.ai_settings.pipe_width<bird.x<=pipe.x+pipe.ai_settings.pipe_width+pipe.ai_settings.move_step:
            stat.score+=1
            stat.action_reward=1
def getframe():
    frame=pygame.surfarray.array3d(pygame.display.get_surface())
    return frame
def phi(image):
    image=cv2.cvtColor(cv2.resize(image,(84,84)),cv2.COLOR_BGR2GRAY)
    ret,image=cv2.threshold(image,1,255,cv2.THRESH_BINARY)
    return image