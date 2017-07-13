from PIL import Image
import numpy as np
import pygame

base=Image.open('sprites/pipe-green.png','r')
screen=Image.open('sprites/background-black.png','r')
base1=base.rotate(180)
base=np.asarray(base)
print(base)
sc=np.asarray(screen)
base1=np.asarray(base1)
print(base.shape,base1.shape)