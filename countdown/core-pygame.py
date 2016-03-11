# -*- coding: utf-8 -*-
import pygame
import time
from pyscope import pyscope
from Counter import Counter
import argparse
import sys
from pygame.locals import *

IS_READY = True
INITIAL_COUNTER = 300
WARNING_LIMIT = 60
DANGER_LIMIT = 30
WELCOME_TIME = 1

class Core:
    def __init__(self, args):
        self.args = self._parse_args(args)
        self.counter = Counter(self.args.counter, self.args.warning, self.args.danger)
        self.scope = self._init_scope()
        self.done = False

    def run(self):
        self._show_welcome()
        self._show_title()
        self._main_loop()

    def _parse_args(self, args):
        parser = argparse.ArgumentParser(description='Start a countdown interactive interface.')
        parser.add_argument('--counter', '-c', type=int, default=INITIAL_COUNTER, help='Amount of seconds for the timer')
        parser.add_argument('--warning', '-w', type=int, default=WARNING_LIMIT, help='Time limit to start warning signal')
        parser.add_argument('--danger', '-d', type=int, default=DANGER_LIMIT, help='Time limit to start danger signal')
        return parser.parse_args(args)

    def _init_scope(self):
        # Create an instance of the PyScope class
        scope = pyscope()
        pygame.display.set_caption('#HMU Timer')
        # Optimizing
        pygame.event.set_allowed([QUIT, KEYDOWN])
        scope.screen.set_alpha(None)
        return scope

    def _show_welcome(self):
        # Display welcome text
        font = pygame.font.Font(None, 512)
        text = font.render("#HMU28", 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = self.scope.screen.get_rect().centerx
        textpos.centery = self.scope.screen.get_rect().centery
        self.scope.screen.blit(text, textpos)
        pygame.display.flip()
        time.sleep(WELCOME_TIME)

    def _show_title(self):
        # Display title text
        self.scope.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 128)
        titleText = font.render("#HMU28", 1, (255, 255, 255))
        titleTextpos = titleText.get_rect()
        titleTextpos.centerx = self.scope.screen.get_rect().width - titleTextpos.width // 2 - 100
        titleTextpos.centery = 100
        self.scope.screen.blit(titleText, titleTextpos)
        pygame.display.flip()

    def _main_loop(self):
        # Main loop
        lastText = None
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    break
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                    elif event.key == K_SPACE:
                        if self.counter.isRunning():
                            self.counter.stop()
                        else:
                            self.counter.start()
                    elif event.key == K_r or event.key == K_UP:
                        self.counter.reset()
            pygame.event.pump()

            if IS_READY:
                if lastText == None or self.counter.text != lastText:
                    print "Repaint " + self.counter.text
                    self.scope.screen.fill((0, 0, 0))
                    rectangle = self._draw_counter()
                    # Repaint middle section
                    pygame.display.update(pygame.Rect(0, rectangle.top, self.scope.screen.get_rect().width, rectangle.height))
                lastText = self.counter.text
                self.counter.update()


    def _draw_counter(self):
        # Display some text
        font = pygame.font.Font(None, 512)
        text = font.render(self.counter.text, 1, self.counter.color)
        textpos = text.get_rect()
        textpos.centerx = self.scope.screen.get_rect().centerx
        textpos.centery = self.scope.screen.get_rect().centery
        self.scope.screen.blit(text, textpos)
        #background.blit(titleText, titleTextpos)
        return textpos

if __name__ == "__main__":
    core = Core(sys.argv[1:])
    core.run()