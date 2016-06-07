from random import randint

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


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
