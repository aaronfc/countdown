from __future__ import unicode_literals
from random import randint, choice

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader

from countdown.components.Heart import HeartImage
from countdown.components.Poo import PooImage
from countdown.config import MAX_HEART_ANGLE
from countdown.sources.External import External, ExternalEvents
from countdown.components.Counter import CounterEvents

class MainScreen(Screen):
    counter_widget = ObjectProperty(None)
    hearts = []

    def __init__(self, counter, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.external = External()
        self.counter = counter
        self.running = False
        self.timeout_sound = SoundLoader.load('assets/end-game-fail.wav')

    def update(self, dt):
        if self.running:
            events = self.counter.update()
            self.counter_widget.update(self.counter.text, self.counter.color)
            events.extend(self.external.get_events())
            self.__handle_events(events)
            self.__update_hearts(dt)

    def on_enter(self):
        self.running = True
        self._keyboard = Window.request_keyboard(self.__keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.__on_keyboard_down)
        self.external.start()

    def on_leave(self):
        self.external.stop()
        self.running = False
        Window.release_all_keyboards()

    '''
     PRIVATE METHODS
    '''

    def __handle_events(self, events):
        for event in events:
            if event == ExternalEvents.NEW_HEART:
                self.__add_new_heart()
            elif event == ExternalEvents.NEW_POO:
                self.__add_new_poo()
            elif event == CounterEvents.STATUS_CHANGE_TIME_OUT:
                self.__play_timeout_sound()

    def __update_hearts(self, dt):
        # This seems like na overkill update loop. They might be updated in batches somehow.
        for heart in self.hearts:
            heart.update(dt)
            if heart.opacity <= 0:
                self.remove_widget(heart)
        self.hearts = [heart for heart in self.hearts if heart.opacity > 0]

    def __play_timeout_sound(self):
        self.timeout_sound.play()

    def __add_new_heart(self):
        position = (randint(0, self.width), randint(0, self.height))
        random_size = randint(60, 120)
        size = [random_size, random_size]
        color = [randint(0, 100)/100., randint(0, 100)/100., randint(0, 100)/100., 1]
        wimg = HeartImage(angle=randint(-MAX_HEART_ANGLE, MAX_HEART_ANGLE), center=position, size=size, color=color)
        self.add_widget(wimg)
        self.hearts.append(wimg)

    def __add_new_poo(self):
        position = (randint(0, self.width), randint(0, self.height))
        random_size = randint(60, 120)
        size = [random_size, random_size]
        wimg = PooImage(angle=randint(-MAX_HEART_ANGLE, MAX_HEART_ANGLE), center=position, size=size)
        self.add_widget(wimg)
        self.hearts.append(wimg)

    def __keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.__on_keyboard_down)
        self._keyboard = None

    def __on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "s":
            if self.counter.isRunning():
                # print "Stopping"
                self.counter.stop()
            else:
                # print "Starting"
                self.counter.start()
        elif keycode[1] == 'r':
            # print "Resetting"
            self.counter.reset()
        elif keycode[1] == 'h':
            # print "Heart created manually"
            self.__add_new_heart()
        elif keycode[1] == 'x':
            # print "Heart created manually"
            self.__add_new_poo()
        elif keycode[1] == 'escape':
            self.counter.stop()
            self.counter.reset()
            self.manager.current = 'welcome'
            # print "Back to welcome"
        return True
