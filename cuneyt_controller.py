from cuneyt import cuneyt
import pygame
import time
from pygame.locals import *
from sys import exit
import random

pygame.init()
screen=pygame.display.set_mode((1024,718),0,32)
pygame.display.set_caption("Cuneyt Joystick Controller")
back = pygame.Surface((1024,718))
background = back.convert()
background.fill((0,0,0))

c = cuneyt(motor_setup=1,motor_driver=0)
while True:
  V = 0
  W = 0
  screen.blit(background,(0,0))
  V += pygame.key.get_pressed()[pygame.K_UP]
  V -= pygame.key.get_pressed()[pygame.K_DOWN]
  W += pygame.key.get_pressed()[pygame.K_LEFT]
  W -= pygame.key.get_pressed()[pygame.k_RIGHT]
  c.motors.move(V,W)
