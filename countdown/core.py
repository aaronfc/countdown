# -*- coding: utf-8 -*-
import sys

from components.Counter import CounterOptions
from config import FULLSCREEN

# Load arguments
options = CounterOptions().load(sys.argv[1:])

if options.DEBUG:
    from kivy.config import Config
    Config.set('modules', 'monitor', 'true')

from components.Counter import Counter
from components.App import CountdownApp
from kivy.core.window import Window

# Display configurations
Window.fullscreen = FULLSCREEN

counter = Counter(options)
CountdownApp(counter).run()
