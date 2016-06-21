from random import randint

from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class HeartsSummary(Widget):
    hearts_num = NumericProperty()

    def update(self, dt):
        self.ids.counter_label.text = text
        self.opacity -= 0.01
        self.center = (self.center[0] + randint(1, 1) * self.direction, self.center[1] + randint(1, 5))
        self.angle += self.direction
        self._update_direction()

    def _update_direction(self):
        if self.direction == 1 and self.angle >= MAX_HEART_ANGLE:
            self.direction = -1
        elif self.direction == -1 and self.angle <= -MAX_HEART_ANGLE:
            self.direction = 1
