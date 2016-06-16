# -*- coding: utf-8 -*-
from time import sleep
import threading
from socketIO_client import SocketIO


class LoveSocket:
    def __init__(self):
        self.io = None
        self.hearts = 0

    def start(self):
        self.io = SocketIO("https://tranquil-dusk-16736.herokuapp.com", verify=False)
        self.io.on("love", self.__add_love)
        threading.Thread(target=self.io.wait).start()

    def stop(self):
        self.io.disconnect()
        self.io = None

    def get_and_reset(self):
        hearts = self.hearts
        self.hearts = 0
        return hearts

    def __add_love(self, *args):
        self.hearts += 1


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    import threading

    love_socket = LoveSocket()
    love_socket.start()
    try:
        while True:
            hearts = love_socket.get_and_reset()
            if hearts > 0:
                print u"♥" * hearts
            sleep(0.1)
    except KeyboardInterrupt:
        love_socket.stop()
