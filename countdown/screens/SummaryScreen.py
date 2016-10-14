from kivy.uix.screenmanager import Screen

from countdown.components.Heart import HeartImage


class SummaryScreen(Screen):
    def __init__(self, **kwargs):
        super(SummaryScreen, self).__init__(**kwargs)

    def move_to_main(self, dt):
        self.manager.current = 'main'


if __name__ == "__main__":
    from kivy.app import App
    from kivy.lang import Builder

    from kivy.factory import Factory
    from countdown.components import HeartsSummary
    Factory.register('HeartsSummary', cls=HeartsSummary)
    Factory.register('HeartImage', cls=HeartImage)

    Builder.load_file("../components/countdown.kv")

    class TestApp(App):
        def build(self):
            screen = SummaryScreen(name='summary')
            return screen

    app = TestApp()
    app.run()