# -*- coding: utf-8 -*-
import pygame
import time
import random
from pyscope import pyscope

# Create an instance of the PyScope class
scope = pyscope()
screen = scope.screen
pygame.display.set_caption('#HMU Timer')

# Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# Display some text
font = pygame.font.Font(None, 256)
text = font.render("Hello!", 1, (255, 255, 255))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
background.blit(text, textpos)

screen.blit(background, (0,0))
pygame.display.flip()

time.sleep(10)