import pygame
from settings import Settings
import game_functions as gf
from base import Base
from pygame.sprite import Group
from bird import Bird
import game_stats
def game_initialize():
    pygame.init()
    ai_settings=Settings()
    pygame.display.set_caption("Flappy Bird")
    base=Base(ai_settings)
    bird=Bird(ai_settings)
    pipes=Group()
    uppipes=Group()
    stat=game_stats.GameStat()
    gf.create_pipes(ai_settings, pipes, uppipes)
    return bird,base,ai_settings,pipes,uppipes,stat
def run_step(bird,base,ai_settings,pipes,uppipes,stat):
    gf.check_event(bird,stat)
    base.update(ai_settings)
    bird.update(stat)
    gf.update_pipes(ai_settings,pipes,uppipes)
    gf.check_crash(bird,pipes,uppipes,base,stat)
    gf.update_screen(ai_settings,base,pipes,uppipes,bird)
    gf.score(bird,pipes,stat)
    stat.xt1 = gf.getframe()
def run_game():
    bird,base,ai_settings,pipes,uppipes,stat=game_initialize()
    while True:
        run_step(bird,base,ai_settings,pipes,uppipes,stat)