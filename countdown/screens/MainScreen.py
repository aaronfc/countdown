from __future__ import unicode_literals
from random import randint, choice

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label

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
        self.summary_widgets = []
        self.hearts_count = 0
        self.poos_count = 0

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
        self.hearts_count = 0
        self.poos_count = 0

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
                # Hearts
                position = (self.width*4/10, self.height/4)
                random_size = 100
                size = [random_size, random_size]
                color = [1., 0., 0., 1]
                wimg = HeartImage(angle=0, center=position, size=size, color=color)
                self.add_widget(wimg)
                label = Label(text="{}".format(self.hearts_count), center=(position[0], position[1] - random_size*3/4), size=(100, 100), size_hint=(None, None), font_size=50)
                self.add_widget(label)
                self.summary_widgets.append(label)
                self.summary_widgets.append(wimg)
                # Poos
                position = (self.width*6/10, self.height/4)
                random_size = 100
                size = [random_size, random_size]
                wimg = PooImage(angle=0, center=position, size=size)
                self.add_widget(wimg)
                label = Label(text="{}".format(self.poos_count), center=(position[0], position[1] - random_size*3/4), size=(100, 100), size_hint=(None, None), font_size=50)
                self.add_widget(label)
                self.summary_widgets.append(label)
                self.summary_widgets.append(wimg)

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
        self.hearts_count += 1

    def __add_new_poo(self):
        position = (randint(0, self.width), randint(0, self.height))
        random_size = randint(60, 120)
        size = [random_size, random_size]
        wimg = PooImage(angle=randint(-MAX_HEART_ANGLE, MAX_HEART_ANGLE), center=position, size=size)
        self.add_widget(wimg)
        self.hearts.append(wimg)
        self.poos_count += 1

    def __keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.__on_keyboard_down)
        self._keyboard = None

    def __on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "s" or keycode[1] == "spacebar":
            if self.counter.isRunning():
                # print "Stopping"
                self.counter.stop()
            else:
                # print "Starting"
                self.counter.start()
                self.hearts_count = 0
                self.poos_count = 0
                for widget in self.summary_widgets:
                    self.remove_widget(widget)
        elif keycode[1] == 'r':
            # print "Resetting"
            self.counter.reset()
            self.hearts_count = 0
            self.poos_count = 0
            for widget in self.summary_widgets:
                self.remove_widget(widget)
        elif keycode[1] == 'h':
            # print "Heart created manually"
            self.__add_new_heart()
        elif keycode[1] == 'x':
            # print "Poo created manually"
            self.__add_new_poo()
        elif keycode[1] == 'escape':
            self.counter.stop()
            self.counter.reset()
            self.hearts_count = 0
            self.poos_count = 0
            for widget in self.summary_widgets:
                self.remove_widget(widget)
            self.manager.current = 'welcome'
            # print "Back to welcome"
        return True
