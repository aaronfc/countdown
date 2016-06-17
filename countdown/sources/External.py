# -*- coding: utf-8 -*-
from enum import Enum
from time import sleep
from LoveSocket import LoveSocket


class ExternalEvents(Enum):
    NEW_HEART = u"♥"
    NEW_POO = u"💩"


class External:
    def __init__(self):
        self.love_socket = LoveSocket()
        self.events = []

    def get_events(self):
        events = [ExternalEvents.NEW_HEART] * self.love_socket.reset_hearts()
        events.extend([ExternalEvents.NEW_POO] * self.love_socket.reset_poos())
        return events

    def start(self):
        self.love_socket.start()

    def stop(self):
        self.love_socket.stop()

if __name__ == "__main__":
    external = External()
    external.start()
    try:
        while True:
            print external.get_events()
            sleep(0.1)
    except KeyboardInterrupt:
        external.stop()