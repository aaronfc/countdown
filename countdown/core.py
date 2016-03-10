# -*- coding: utf-8 -*-
import pyglet
from pyglet.window import key
import time
import random
import math

INITIAL_COUNTER_TIME = 5 # 5 minutes
WARNING_LIMIT = 30
DANGER_LIMIT = 10
WELCOME_TIME = 5
SHOW_FPS = True
IS_READY = False

class Counter():
    def __init__(self, initialValue, warningLimit, dangerLimit, label):
        self.label = label
        self.initialValue = initialValue
        self.running = False
        self.currentValue = initialValue
        self.dangerLimit = dangerLimit
        self.warningLimit = warningLimit
        self.lastTick = None

    def start(self):
        if self.currentValue == 0:
            self.currentValue = self.initialValue
        self.lastTick = time.time()
        if not self.running:
            self.running = True

    def reset(self):
        self.lastTick = time.time()
        self.currentValue = self.initialValue

    def stop(self):
        self.running = False

    def update(self):
        if not IS_READY:
            return
        if self.running:
            newTick = time.time()
            self.currentValue -= newTick - self.lastTick
            self.lastTick = newTick
        if self.currentValue > 0:
            usefulValue = math.ceil(self.currentValue)
            if usefulValue <= self.dangerLimit:
                label.color = (255,50,50,255)
            elif usefulValue <= self.warningLimit:
                label.color = (255,255,100,255)
            else:
                label.color = (255, 255, 255, 255)
            self.label.text = time.strftime("%Mm%Ss", time.gmtime(usefulValue))
        else:
            self.currentValue = 0
            self.running = False
            self.label.text = "TIME'S UP!"
            #self.label.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            self.label.color = (148, 190, 0, random.randint(200, 255))

    def draw(self):
        self.label.draw()

    def isRunning(self):
        return self.running

    def getValue(self):
        return self.currentValue


startTime = time.time()

# FPS display
fps_display = pyglet.clock.ClockDisplay(
    format='%(fps).1f',
    color=(0.2, 0.2, 0.2, 1)
)
# Game window definition
window = pyglet.window.Window(fullscreen=True)
pyglet.gl.glClearColor(0, 0, 0, 1)

label = pyglet.text.Label("#HMU28",
                          font_name='Tahoma',
                          font_size=256,
                          x=window.width // 2, y=window.height // 2,
                          anchor_x='center', anchor_y='center')

labelTitle = pyglet.text.Label("#HMU28",
                          font_name='Tahoma',
                          font_size=64,
                          x=window.width - (window.height // 16), y=window.height // 16 * 15,
                          anchor_x='right', anchor_y='top')

counter = Counter(INITIAL_COUNTER_TIME, WARNING_LIMIT, DANGER_LIMIT, label)

@window.event
def on_draw():
    window.clear()
    if SHOW_FPS:
        fps_display.draw()
    if IS_READY:
        labelTitle.draw()
    counter.draw()

@window.event
def on_key_press(symbol, modifiers):
    if IS_READY:
        if symbol == key.SPACE:
            if counter.isRunning():
                counter.stop()
            else:
                counter.start()
        elif symbol == key.R:
            counter.reset()


def update(dt):
    global IS_READY
    if not IS_READY:
        IS_READY = (time.time() - startTime) > WELCOME_TIME
    counter.update()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 0.5)
    pyglet.app.run()