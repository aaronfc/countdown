# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from random import randint
from Counter import Counter, CounterOptions, CounterEvents
from External import External, ExternalEvents
import sys

# Configuration
FULLSCREEN = False
MAX_HEART_ANGLE = 20


# TODO Extract heart moving logic to a Heart instance with update(dt) method and let this only be the representation
class HeartImage(Image):
    angle = NumericProperty()
    direction = 1 if randint(0, 1) == 1 else -1

    def update(self, dt):
        self.opacity -= 0.01
        self.center = (self.center[0] + randint(1, 1) * self.direction, self.center[1] + randint(1, 5))
        self.angle += self.direction
        self._update_direction()

    def _update_direction(self):
        if self.direction == 1 and self.angle >= MAX_HEART_ANGLE:
            self.direction = -1
        elif self.direction == -1 and self.angle <= -MAX_HEART_ANGLE:
            self.direction = 1


class CounterWidget(Widget):
    def __init__(self, **kwargs):
        super(CounterWidget, self).__init__(**kwargs)

    def update(self, text, color):
        self.ids.counter_label.text = text
        self.ids.counter_label.color = (color[0]/255., color[1]/255., color[2]/255., 1)


class MainScreen(Screen):
    counter_widget = ObjectProperty(None)
    external = External()
    hearts = []

    def __init__(self, counter, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.counter = counter
        self.running = False

    def update(self, dt):
        if self.running:
            events = self.counter.update()
            self.counter_widget.update(self.counter.text, self.counter.color)
            events.extend(self.external.get_events())
            self.handle_events(events)
            # This seems like a overkill update loop. They might be updated in batches somehow.
            for heart in self.hearts:
                heart.update(dt)

    def on_enter(self):
        self.running = True
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self):
        self.running = False
        Window.release_all_keyboards()

    def handle_events(self, events):
        for event in events:
            if event == ExternalEvents.NEW_HEART:
                self._add_new_heart()

    def _add_new_heart(self):
        position = (randint(self.width/2, self.width), randint(0, self.height/2))
        random_size = randint(30, 60)
        size = [random_size, random_size]
        color = [randint(0, 100)/100., randint(0, 100)/100., randint(0, 100)/100., 1]
        # print "New heart at {} with size {} and color {}".format(position, random_size, color)
        wimg = HeartImage(angle=randint(-MAX_HEART_ANGLE, MAX_HEART_ANGLE), center=position, size=size, color=color)
        self.add_widget(wimg)
        self.hearts.append(wimg)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
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
            self._add_new_heart()
        elif keycode[1] == 'escape':
            self.counter.stop()
            self.counter.reset()
            self.manager.current = 'welcome'
            # print "Back to welcome"
        return True


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.set_title(randint(10, 50))
        self.first_time = True

    def on_enter(self):
        if self.first_time:
            Clock.schedule_once(self.move_to_main, 3)

    def set_title(self, num):
        self.ids.title_label.text = "#HMU" + str(num)

    def move_to_main(self, dt):
        self.first_time = False
        self.manager.current = 'main'


class CountdownApp(App):

    def __init__(self, counter):
        super(CountdownApp, self).__init__()
        self.counter = counter

    def build(self):
        # Create screens
        main_screen = MainScreen(counter, name='main')
        welcome_screen = WelcomeScreen(name='welcome')
        # Create the screen manager
        sm = ScreenManager(transition=FallOutTransition())
        sm.add_widget(welcome_screen)
        sm.add_widget(main_screen)
        # Setup main screen updater
        Clock.schedule_interval(main_screen.update, 1.0/60.0)
        return sm


if __name__ == '__main__':

    # Instantiate counter
    options = CounterOptions().load(sys.argv[1:])
    counter = Counter(options)

    # Display configurations
    Window.fullscreen = FULLSCREEN

    CountdownApp(counter).run()
