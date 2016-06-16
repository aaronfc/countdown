# -*- coding: utf-8 -*-
from enum import Enum
from time import sleep
from LoveSocket import LoveSocket


class ExternalEvents(Enum):
    NEW_HEART = u"♥"


class External:
    def __init__(self):
        self.love_socket = LoveSocket()
        self.events = []

    def get_events(self):
        events = [ExternalEvents.NEW_HEART] * self.love_socket.get_and_reset()
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