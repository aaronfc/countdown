from random import randint

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from countdown.components.Heart import HeartImage
from countdown.config import MAX_HEART_ANGLE
from countdown.sources.External import External, ExternalEvents


class MainScreen(Screen):
    counter_widget = ObjectProperty(None)
    hearts = []

    def __init__(self, counter, queue, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.external = External(queue)
        self.counter = counter
        self.running = False

    def update(self, dt):
        if self.running:
            events = self.counter.update()
            self.counter_widget.update(self.counter.text, self.counter.color)
            events.extend(self.external.get_events())
            self.handle_events(events)
            # This seems like na overkill update loop. They might be updated in batches somehow.
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
        position = (randint(0, self.width), randint(0, self.height))
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
