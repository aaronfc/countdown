from enum import Enum


class ExternalEvents(Enum):
    NEW_HEART = 'heart'


class External:
    def __init__(self, queue):
        self.queue = queue

    def get_events(self):
        events = []

        if not self.queue.empty():
            element = self.queue.get_nowait()
            if element is not None:
                events.append(ExternalEvents.NEW_HEART)

        return events
