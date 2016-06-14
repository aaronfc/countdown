# -*- coding: utf-8 -*-
import sys
from kivy.core.window import Window

from components.App import CountdownApp
from components.Counter import Counter, CounterOptions
from config import FULLSCREEN
from countdown.server import Server
from Queue import Queue

if __name__ == '__main__':

    queue = Queue()

    # Instantiate counter
    options = CounterOptions().load(sys.argv[1:])
    counter = Counter(options)

    # Display configurations
    Window.fullscreen = FULLSCREEN

    # Initiate web server
    server = Server(queue)
    server.start(9999)

    CountdownApp(counter, queue).run()
