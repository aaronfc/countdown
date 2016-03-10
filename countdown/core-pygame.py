# -*- coding: utf-8 -*-
import pygame
import random
import time
from pyscope import pyscope
from Counter import Counter
from pygame.locals import *

DONE = False
IS_READY = True
INITIAL_COUNTER = 300
WARNING_LIMIT = 60
DANGER_LIMIT = 30
WELCOME_TIME = 1

# Create an instance of the PyScope class
scope = pyscope()
screen = scope.screen
pygame.display.set_caption('#HMU Timer')
# Optimizing
pygame.event.set_allowed([QUIT, KEYDOWN])
screen.set_alpha(None)

# Initialize background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

# Display welcome text
font = pygame.font.Font(None, 512)
text = font.render("#HMU28", 1, (255, 255, 255))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
textpos.centery = background.get_rect().centery
background.blit(text, textpos)
screen.blit(background, (0,0))
pygame.display.flip()
time.sleep(WELCOME_TIME)

counter = Counter(INITIAL_COUNTER, WARNING_LIMIT, DANGER_LIMIT)

def draw(background, counter):
    # Display title text
    font = pygame.font.Font(None, 128)
    text = font.render("#HMU28", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().width - textpos.width // 2 - 100
    textpos.centery = 100
    background.blit(text, textpos)
    # Display some text
    font = pygame.font.Font(None, 512)
    text = font.render(counter.text, 1, counter.color)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)

# Main loop
lastText = None
while not DONE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                DONE = True
            elif event.key == K_SPACE:
                if counter.isRunning():
                    counter.stop()
                else:
                    counter.start()
            elif event.key == K_r:
                counter.reset()

    background.fill((0, 0, 0))
    if IS_READY:
        if lastText == None or counter.text != lastText:
            draw(background, counter)
            screen.blit(background, (0, 0))
            pygame.display.flip()
        lastText = counter.text
        counter.update()