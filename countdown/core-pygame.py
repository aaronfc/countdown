# -*- coding: utf-8 -*-
import pygame
import random
import time
from pyscope import pyscope
from Counter import Counter
import pprint
from pygame.locals import *

DONE = False
IS_READY = True
INITIAL_COUNTER = 10
WARNING_LIMIT = 5
DANGER_LIMIT = 3
WELCOME_TIME = 1

# Create an instance of the PyScope class
scope = pyscope()
screen = scope.screen
pygame.display.set_caption('#HMU Timer')
# Optimizing
pygame.event.set_allowed([QUIT, KEYDOWN])
screen.set_alpha(None)

# Display welcome text
font = pygame.font.Font(None, 512)
text = font.render("#HMU28", 1, (255, 255, 255))
textpos = text.get_rect()
textpos.centerx = screen.get_rect().centerx
textpos.centery = screen.get_rect().centery
screen.blit(text, textpos)
pygame.display.flip()
time.sleep(WELCOME_TIME)

# Display title text
screen.fill((0, 0, 0))
font = pygame.font.Font(None, 128)
titleText = font.render("#HMU28", 1, (255, 255, 255))
titleTextpos = titleText.get_rect()
titleTextpos.centerx = screen.get_rect().width - titleTextpos.width // 2 - 100
titleTextpos.centery = 100
screen.blit(titleText, titleTextpos)
pygame.display.flip()

counter = Counter(INITIAL_COUNTER, WARNING_LIMIT, DANGER_LIMIT)

def draw(background, counter):
    # Display some text
    font = pygame.font.Font(None, 512)
    text = font.render(counter.text, 1, counter.color)
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)
    background.blit(titleText, titleTextpos)
    return textpos

# Main loop
lastText = None
while not DONE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
            break
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                DONE = True
                break
            elif event.key == K_SPACE:
                if counter.isRunning():
                    counter.stop()
                else:
                    counter.start()
                break
            elif event.key == K_r or event.key == K_UP:
                counter.reset()
                break
    pygame.event.pump()

    if IS_READY:
        if lastText == None or counter.text != lastText:
            print "Repaint " + counter.text
            screen.fill((0, 0, 0))
            rectangle = draw(screen, counter)
            # Repaint middle section
            pygame.display.update(pygame.Rect(0, rectangle.top, screen.get_rect().width, rectangle.height))
        lastText = counter.text
        counter.update()