# -*- coding: utf-8 -*-
import sys
from kivy.core.window import Window

from components.App import CountdownApp
from components.Counter import Counter, CounterOptions
from config import FULLSCREEN

if __name__ == '__main__':

    # Instantiate counter
    options = CounterOptions().load(sys.argv[1:])
    counter = Counter(options)

    # Display configurations
    Window.fullscreen = FULLSCREEN

    CountdownApp(counter).run()
