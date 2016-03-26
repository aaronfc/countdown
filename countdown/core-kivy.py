# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from random import randint
from Counter import Counter, CounterEvents
from External import External, ExternalEvents

FULLSCREEN = False


class HeartImage(Image):
    angle = NumericProperty()
    direction = 1 if randint(0, 1) == 1 else -1

    def update(self, dt):
        self.opacity -= 0.01
        self.center = (self.center[0] + randint(-5, 5), self.center[1] + randint(1, 5))
        self.angle = self.angle + self.direction
        self._update_direction()

    def _update_direction(self):
        if self.direction == 1 and self.angle >= 30:
            self.direction = -1
        elif self.direction == -1 and self.angle <= -30:
            self.direction = 1


class CounterWidget(Widget):

    def __init__(self, **kwargs):
        super(CounterWidget, self).__init__(**kwargs)
        self.counter = Counter(10, 5, 3)

    def update(self, dt):
        events = self.counter.update()
        self.ids.counter_label.text = self.counter.text
        self.ids.counter_label.color = (self.counter.color[0]/255., self.counter.color[1]/255., self.counter.color[2]/255., 1)
        return events


class MainScreen(Screen):
    counter = ObjectProperty(None)
    external = External()
    hearts = []

    def update(self, dt):
        events = self.counter.update(dt)
        events.extend(self.external.get_events())
        self.handle_events(events)
        for heart in self.hearts:
            heart.update(dt)



    def on_enter(self):
        print "Binding keyboard"
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self):
        Window.release_all_keyboards()
        pass

    def handle_events(self, events):
        for event in events:
            if event == ExternalEvents.NEW_HEART:
                self._add_heart()

    def _add_heart(self):
        print "Self width: {}".format(self.width)
        position = (randint(0, self.width), randint(0, self.height))
        random_size = randint(30, 60)
        print "New heart at {} with size {}".format(position, random_size)
        size = [random_size, random_size]
        color = [randint(0, 100)/100., randint(0, 100)/100., randint(0, 100)/100., 1]
        print color
        wimg = HeartImage(angle=randint(-30, 30), center=position, size=size, color=color)
        self.add_widget(wimg)
        self.hearts.append(wimg)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "s":
            if self.counter.counter.isRunning():
                print "Stopping"
                self.counter.counter.stop()
            else:
                print "Starting"
                self.counter.counter.start()
        elif keycode[1] == 'r':
            print "Resetting"
            self.counter.counter.reset()
        elif keycode[1] == 'h':
            print "Heart!"
            self._add_heart()
        elif keycode[1] == 'escape':
            self.counter.counter.stop()
            self.counter.counter.reset()
            self.manager.current = 'welcome'
            print "Exiting"
        return True


class WelcomeScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(self.move_to_main, 3)

    def set_title(self):
        self.ids.title_label.text = "#HMU" + str(randint(20, 50))

    def move_to_main(self, dt):
        self.manager.current = 'main'


class CountdownApp(App):
    def build(self):
        # Create screens
        main_screen = MainScreen(name='main')
        welcome_screen = WelcomeScreen(name='welcome')
        welcome_screen.set_title()
        # Create the screen manager
        sm = ScreenManager(transition=FallOutTransition())
        sm.add_widget(welcome_screen)
        sm.add_widget(main_screen)
        # Setup main screen updater
        Clock.schedule_interval(main_screen.update, 1.0/60.0)
        return sm


if __name__ == '__main__':
    Window.fullscreen = FULLSCREEN
    CountdownApp().run()
