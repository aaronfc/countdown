from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, FallOutTransition

from ..screens.MainScreen import MainScreen
from ..screens.WelcomeScreen import WelcomeScreen


class CountdownApp(App):

    def __init__(self, counter):
        super(CountdownApp, self).__init__()
        self.counter = counter

    def build(self):
        # Create screens
        main_screen = MainScreen(self.counter, name='main')
        welcome_screen = WelcomeScreen(name='welcome')
        # Create the screen manager
        sm = ScreenManager(transition=FallOutTransition())
        sm.add_widget(welcome_screen)
        sm.add_widget(main_screen)
        # Setup main screen updater
        Clock.schedule_interval(main_screen.update, 1.0/60.0)
        return sm
