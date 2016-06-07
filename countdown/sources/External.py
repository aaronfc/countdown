from enum import Enum
from random import randint


class ExternalEvents(Enum):
    NEW_HEART = 'heart'


class External:
    def __init__(self):
        pass

    def get_events(self):
        events = []
        num = randint(0, 100)
        #print "Generating " + str(num)
        if num < 1:
            events.append(ExternalEvents.NEW_HEART)
        return events
