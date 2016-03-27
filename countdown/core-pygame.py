# -*- coding: utf-8 -*-
import pygame
import time
from pyscope import pyscope
from Counter import Counter, CounterOptions, CounterEvents
from External import External, ExternalEvents
import argparse
import sys
import random
from pygame.locals import *

IS_READY = True
INITIAL_COUNTER = 300
WARNING_LIMIT = 60
DANGER_LIMIT = 30
WELCOME_TIME = 1

class Core:
    def __init__(self, args):
        self.external = External()
        self.ops = self._parse_args(args)
        self.scope = self._init_scope()
        self.sounds = self._init_sounds()
        self.counter = Counter(self.ops)
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
        parsed = parser.parse_args(args)
        options = CounterOptions()
        options.DANGER_LIMIT = parsed.danger
        options.WARNING_LIMIT = parsed.warning
        options.INITIAL_COUNTER = parsed.counter
        return options


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
                    if event.key == K_ESCAPE or event.key == K_q:
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
                    self.scope.screen.fill((0, 0, 0))
                    rectangle = self._draw_counter()
                    # Repaint middle section
                    pygame.display.update(pygame.Rect(0, rectangle.top, self.scope.screen.get_rect().width, rectangle.height))
                lastText = self.counter.text
                events = self.counter.update()
                events.extend(self.external.get_events())
                self._handle_events(events)

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

    def _init_sounds(self):
        sounds = dict()
        sounds['time-out'] = pygame.mixer.Sound('emergency006.wav')
        return sounds

    def _handle_events(self, events):
        for event in events:
            # Sounds
            if event == CounterEvents.STATUS_CHANGE_TIME_OUT:
                self.sounds['time-out'].play()
            elif event == ExternalEvents.NEW_HEART:
                self._add_heart()

    def _add_heart(self):
        rectangles = []
        point = (random.randint(0, self.scope.screen.get_rect().width), random.randint(0, self.scope.screen.get_rect().height))
        size = random.randint(20, 100)
        # Ugly heart definition
        rectangles.append(pygame.draw.polygon(self.scope.screen, (255, 0, 0), [(point[0]-size/2, point[1]), (point[0]+size/2, point[1]), (point[0], point[1]+size/2)]))
        rectangles.append(pygame.draw.circle(self.scope.screen, (255, 0, 0), (point[0]+size/4, point[1]-2), size/4-1))
        rectangles.append(pygame.draw.circle(self.scope.screen, (255, 0, 0), (point[0]-size/4, point[1]-2), size/4-1))
        # Repaint
        pygame.display.update(rectangles)


if __name__ == "__main__":
    core = Core(sys.argv[1:])
    core.run()