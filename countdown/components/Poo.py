from random import randint

from kivy.properties import NumericProperty
from kivy.uix.image import Image


# TODO Extract heart moving logic to a Heart instance with update(dt) method and let this only be the representation
from countdown.config import MAX_HEART_ANGLE


class PooImage(Image):
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
