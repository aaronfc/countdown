from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from countdown.config import HMU_EDITION


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.set_title(HMU_EDITION)
        self.first_time = True

    def on_enter(self):
        if self.first_time:
            Clock.schedule_once(self.move_to_main, 3)

    def set_title(self, num):
        self.ids.title_label.text = "#HMU" + str(num)

    def move_to_main(self, dt):
        self.first_time = False
        self.manager.current = 'main'


if __name__ == "__main__":
    from kivy.app import App

    class TestApp(App):
        def build(self):
            self.load_kv("../components/countdown.kv")
            return WelcomeScreen(name='welcome')

    app = TestApp()
    app.run()